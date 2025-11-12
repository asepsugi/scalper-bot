import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from config import CONFIG

"""
Modul ini berisi fungsi-fungsi untuk mendeteksi konsep Smart Money (SMC)
seperti Market Structure, Order Blocks, dan Premium/Discount Zones.
"""

def get_swing_points(df: pd.DataFrame, prominence: float = 0.01):
    """
    Mengidentifikasi swing highs dan swing lows menggunakan `find_peaks`.
    Prominence adalah metrik seberapa menonjol sebuah puncak dari sekitarnya.
    """
    high_peaks_indices, _ = find_peaks(df['high'], prominence=(df['high'].max() - df['high'].min()) * prominence)
    low_peaks_indices, _ = find_peaks(-df['low'], prominence=(df['low'].max() - df['low'].min()) * prominence)
    
    swings = []
    for idx in high_peaks_indices:
        swings.append({'type': 'high', 'time': df.index[idx], 'price': df['high'].iloc[idx]})
    for idx in low_peaks_indices:
        swings.append({'type': 'low', 'time': df.index[idx], 'price': df['low'].iloc[idx]})
        
    if not swings:
        return []
        
    # Urutkan berdasarkan waktu
    swings.sort(key=lambda x: x['time'])
    
    # Hapus swing yang berurutan dengan tipe yang sama (misal: high, high, low -> high, low)
    unique_swings = [swings[0]]
    for i in range(1, len(swings)):
        if swings[i]['type'] != unique_swings[-1]['type']:
            unique_swings.append(swings[i])
            
    return unique_swings

def detect_market_structure(swings: list):
    """
    Mendeteksi Break of Structure (BOS) dan Change of Character (CHoCH).
    Mengembalikan struktur pasar terakhir yang terdeteksi.
    """
    if len(swings) < 4:
        return None, None # Butuh minimal 4 swing points

    structure_points = []
    trend = "UNDETERMINED"
    
    # Iterasi dari belakang untuk mendapatkan struktur terbaru
    for i in range(len(swings) - 2, 1, -1):
        p1, p2, p3 = swings[i-1], swings[i], swings[i+1]

        # Bullish Structure: Higher High (HH)
        if p1['type'] == 'high' and p2['type'] == 'low' and p3['type'] == 'high':
            if p3['price'] > p1['price']: # New HH
                structure_points.append({'type': 'BOS_UP', 'time': p3['time'], 'price': p3['price']})
                trend = "BULLISH"
                break # Ditemukan struktur terbaru

        # Bearish Structure: Lower Low (LL)
        if p1['type'] == 'low' and p2['type'] == 'high' and p3['type'] == 'low':
            if p3['price'] < p1['price']: # New LL
                structure_points.append({'type': 'BOS_DOWN', 'time': p3['time'], 'price': p3['price']})
                trend = "BEARISH"
                break # Ditemukan struktur terbaru

    if not structure_points:
        return None, None

    last_structure = structure_points[0]
    
    # Cari swing terakhir sebelum BOS untuk menentukan Order Block
    last_swing_before_bos = None
    for s in reversed(swings):
        if s['time'] < last_structure['time']:
            last_swing_before_bos = s
            break
            
    return last_structure, last_swing_before_bos

def find_order_block(df: pd.DataFrame, last_swing: dict, structure_type: str):
    """
    REVISED: Menemukan Order Block (OB) yang valid dengan filter yang lebih ketat.
    Sebuah OB valid jika diikuti oleh gerakan impulsif yang dikonfirmasi oleh volume dan candle berurutan.
    """
    if not last_swing or 'time' not in last_swing:
        return None

    cfg = CONFIG['smc_filters']
    atr_col = f"ATRr_{CONFIG['atr_period']}"
    vol_col = f"VOL_{CONFIG['volume_lookback']}"

    try:
        # 1. Tentukan candle OB potensial (candle terakhir berlawanan arah sebelum swing)
        ob_candle_loc = df.index.get_loc(last_swing['time'])
        potential_ob_candle = None
        
        # Cari mundur dari swing point untuk menemukan candle yang berlawanan
        for i in range(ob_candle_loc, max(0, ob_candle_loc - 5), -1):
            candle = df.iloc[i]
            if structure_type == 'BOS_UP' and candle['close'] < candle['open']: # Bullish OB adalah candle bearish
                potential_ob_candle = candle
                break
            elif structure_type == 'BOS_DOWN' and candle['close'] > candle['open']: # Bearish OB adalah candle bullish
                potential_ob_candle = candle
                break
        
        if potential_ob_candle is None:
            return None

        # 2. Validasi Gerakan Impulsif setelah OB
        ob_time = potential_ob_candle.name
        impulse_window = df.loc[ob_time:].iloc[1:] # Candle-candle setelah OB
        if len(impulse_window) < cfg['ob_consecutive_candles']:
            return None

        # Filter 2a: Konfirmasi Candle Berurutan
        consecutive_candles_confirmed = True
        for i in range(cfg['ob_consecutive_candles']):
            impulse_candle = impulse_window.iloc[i]
            if structure_type == 'BOS_UP' and impulse_candle['close'] < impulse_candle['open']:
                consecutive_candles_confirmed = False
                break
            if structure_type == 'BOS_DOWN' and impulse_candle['close'] > impulse_candle['open']:
                consecutive_candles_confirmed = False
                break
        
        if not consecutive_candles_confirmed:
            return None

        # Filter 2b: Konfirmasi Volume & Jarak Impulsif
        first_impulse_candle = impulse_window.iloc[0]
        volume_confirmed = first_impulse_candle['volume'] > (first_impulse_candle[vol_col] * cfg['ob_volume_multiplier'])
        
        price_move = abs(first_impulse_candle['close'] - potential_ob_candle['close'])
        atr_at_ob = potential_ob_candle[atr_col]
        impulse_distance_confirmed = price_move > (atr_at_ob * cfg['ob_impulse_atr_multiplier'])

        # Jika semua filter terpenuhi, OB dianggap valid
        if volume_confirmed and impulse_distance_confirmed:
            return {
                'type': 'BULLISH_OB' if structure_type == 'BOS_UP' else 'BEARISH_OB',
                'start_time': potential_ob_candle.name,
                'top': potential_ob_candle['high'],
                'bottom': potential_ob_candle['low']
            }
            
    except Exception as e:
        # console.log(f"Error in find_order_block: {e}") # Uncomment for debugging
        return None
    return None

def find_fvg(df: pd.DataFrame, last_structure: dict):
    """
    Mencari Fair Value Gap (FVG) terbaru setelah Break of Structure (BOS).
    FVG adalah area inefisiensi harga yang sering diisi kembali.
    """
    if not last_structure:
        return None

    # Cari FVG di sekitar area setelah BOS terjadi
    search_window = df.loc[last_structure['time']:]
    if len(search_window) < 3: return None

    for i in range(len(search_window) - 2, 0, -1):
        c1, c2, c3 = search_window.iloc[i-1], search_window.iloc[i], search_window.iloc[i+1]
        
        # Bullish FVG (celah antara high c1 dan low c3)
        if c1['high'] < c3['low']:
            return {'type': 'BULLISH_FVG', 'top': c3['low'], 'bottom': c1['high']}
        # Bearish FVG (celah antara low c1 dan high c3)
        elif c1['low'] > c3['high']:
            return {'type': 'BEARISH_FVG', 'top': c1['low'], 'bottom': c3['high']}
    return None

def get_premium_discount_zones(df: pd.DataFrame, swings: list):
    """
    Menentukan zona Premium & Discount dari swing high dan low terakhir.
    """
    if len(swings) < 2:
        return None, None, None

    last_two_swings = swings[-2:]
    swing_high = max(s['price'] for s in last_two_swings)
    swing_low = min(s['price'] for s in last_two_swings)
    
    equilibrium = (swing_high + swing_low) / 2
    return swing_high, swing_low, equilibrium

def analyze_smc_on_trend_tf(df_trend: pd.DataFrame):
    """
    Fungsi utama untuk menjalankan semua analisis SMC pada DataFrame timeframe tren.
    Mengembalikan dictionary berisi zona-zona penting.
    """
    if df_trend is None or df_trend.empty or len(df_trend) < 50:
        return {}

    # 1. Dapatkan struktur pasar
    swings = get_swing_points(df_trend, prominence=0.015)
    last_structure, last_swing_before_bos = detect_market_structure(swings)
    
    if not last_structure:
        return {}

    # 2. Dapatkan Order Block
    order_block = find_order_block(df_trend, last_swing_before_bos, last_structure['type'])

    # 3. Dapatkan FVG terbaru
    fvg = find_fvg(df_trend, last_structure)

    # 4. Dapatkan Zona Premium/Discount
    swing_high, swing_low, equilibrium = get_premium_discount_zones(df_trend, swings)

    return {
        "last_structure": last_structure,
        "order_block": order_block,
        "fvg": fvg,
        "equilibrium": equilibrium,
        # --- PENAMBAHAN: Kembalikan swing points terakhir untuk filter jarak ---
        "recent_swing_high": swing_high,
        "recent_swing_low": swing_low
    }