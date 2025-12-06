"""
Diagnostic Script for Scalper Bot
This script helps identify why backtest_market_scanner isn't generating signals.

Usage:
    python diagnostics.py

This will analyze your strategies, data, and configuration to pinpoint issues.
"""

import asyncio
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import sys

from functools import partial # Import partial
# Import your bot modules
try:
    from config import CONFIG, LIVE_TRADING_CONFIG, LEVERAGE_MAP
    from strategies import STRATEGY_CONFIG
    from indicators import calculate_indicators
    from utils.data_preparer import prepare_data
    import ccxt
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running this script from the bot's root directory.")
    sys.exit(1)


class ScalperDiagnostics:
    def __init__(self, start_date=None, end_date=None):
        self.exchange = None
        self.symbols = []
        self.timeframe = CONFIG.get("timeframe_signal", "5m")
        self.limit = 1000  # Start with smaller dataset for diagnostics
        self.start_date = start_date
        self.end_date = end_date
        
    async def initialize_exchange(self):
        """Initialize exchange connection"""
        print("\n" + "="*60)
        print("📊 SCALPER BOT DIAGNOSTICS")
        print("="*60)
        
        try:
            self.exchange = ccxt.binance({
                'enableRateLimit': True,
                'options': {'defaultType': 'future'}
            })
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.exchange.load_markets)
            print("✅ Exchange connection established")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to exchange: {e}")
            return False
    
    async def get_top_symbols(self, count: int = 5) -> List[str]:
        """Get top volume symbols for testing"""
        try:
            loop = asyncio.get_event_loop()
            tickers = await loop.run_in_executor(None, self.exchange.fetch_tickers)
            futures_tickers = {k: v for k, v in tickers.items() if '/USDT' in k and ':USDT' in k}
            
            sorted_tickers = sorted(
                futures_tickers.items(),
                key=lambda x: x[1].get('quoteVolume', 0),
                reverse=True
            )
            
            symbols = [ticker[0] for ticker in sorted_tickers[:count]]
            print(f"✅ Selected top {count} symbols by volume:")
            for i, symbol in enumerate(symbols, 1):
                volume = futures_tickers[symbol].get('quoteVolume', 0)
                print(f"   {i}. {symbol}: ${volume:,.0f}")
            
            return symbols
        except Exception as e:
            print(f"❌ Failed to fetch symbols: {e}")
            return []
    
    async def fetch_and_prepare_data(self, symbol: str) -> pd.DataFrame | None:
        """Fetch and prepare data for a symbol"""
        try:
            # Menggunakan logika multi-timeframe yang sama dengan backtester
            from indicators import fetch_binance_data_sync
            signal_tf = CONFIG['timeframe_signal']
            trend_tf = CONFIG['timeframe_trend']
            if pd.to_timedelta(trend_tf) >= pd.to_timedelta('1h'):
                macro_tf = '4h'
            else:
                macro_tf = '1h'

            # Menggunakan versi sinkron karena kita berada dalam loop async
            loop = asyncio.get_event_loop()

            # PERBAIKAN: Gunakan start_date jika ada, jika tidak, gunakan limit
            if self.start_date:
                print(f"   Fetching data from {self.start_date} to {self.end_date or 'now'}...")
                df_signal, _ = await loop.run_in_executor(None, partial(fetch_binance_data_sync, self.exchange, symbol, signal_tf, start_date=self.start_date, end_date=self.end_date, use_cache=True))
                df_trend, _ = await loop.run_in_executor(None, partial(fetch_binance_data_sync, self.exchange, symbol, trend_tf, start_date=self.start_date, end_date=self.end_date, use_cache=True))
                df_macro, _ = await loop.run_in_executor(None, partial(fetch_binance_data_sync, self.exchange, symbol, macro_tf, start_date=self.start_date, end_date=self.end_date, use_cache=True))
            else:
                buffer = 200
                limit_signal = self.limit
                limit_trend = (limit_signal // max(1, (pd.to_timedelta(trend_tf).total_seconds() / pd.to_timedelta(signal_tf).total_seconds()))) + buffer
                limit_macro = (limit_signal // max(1, (pd.to_timedelta(macro_tf).total_seconds() / pd.to_timedelta(signal_tf).total_seconds()))) + buffer
                df_signal, _ = await loop.run_in_executor(None, partial(fetch_binance_data_sync, self.exchange, symbol, signal_tf, limit=int(limit_signal), use_cache=True))
                df_trend, _ = await loop.run_in_executor(None, partial(fetch_binance_data_sync, self.exchange, symbol, trend_tf, limit=int(limit_trend), use_cache=True))
                df_macro, _ = await loop.run_in_executor(None, partial(fetch_binance_data_sync, self.exchange, symbol, macro_tf, limit=int(limit_macro), use_cache=True))

            if any(df is None or df.empty for df in [df_signal, df_trend, df_macro]):
                print(f"   ❌ Error fetching multi-timeframe data for {symbol}")
                return None
            
            # Gunakan data preparer yang sudah ada
            df = prepare_data(df_signal, df_trend, df_macro)
            
            return df
        except Exception as e:
            print(f"   ❌ Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    def analyze_data_quality(self, df: pd.DataFrame, symbol: str) -> Dict:
        """Analyze data quality and completeness"""
        print(f"\n📈 Data Quality Analysis for {symbol}")
        print("-" * 60)
        
        analysis = {
            'total_candles': len(df),
            'date_range': None,
            'missing_values': {},
            'indicator_readiness': {}
        }
        
        if len(df) > 0:
            analysis['date_range'] = (
                df.index.min().strftime('%Y-%m-%d %H:%M'),
                df.index.max().strftime('%Y-%m-%d %H:%M')
            )
            print(f"   Total Candles: {len(df)}")
            print(f"   Date Range: {analysis['date_range'][0]} to {analysis['date_range'][1]}")
            
            # Check for missing values
            key_columns = ['open', 'high', 'low', 'close', 'volume'] + ['rsi_15m', 'rsi_1h']
            for col in key_columns:
                missing = df[col].isna().sum()
                analysis['missing_values'][col] = missing
                if missing > 0:
                    print(f"   ⚠️  Missing {col}: {missing} values")
            
            # Check indicator calculations
            indicator_cols = [col for col in df.columns if col not in ['open', 'high', 'low', 'close', 'volume']]
            for col in indicator_cols:
                non_null = df[col].notna().sum()
                analysis['indicator_readiness'][col] = non_null
                if non_null < len(df) * 0.5:  # Less than 50% calculated
                    print(f"   ⚠️  Indicator {col}: Only {non_null}/{len(df)} values calculated")
            
            # Check warmup period
            # Gunakan indikator dengan periode terpanjang sebagai proksi
            if 'EMA_200' in df.columns and not df['EMA_200'].isna().all():
                warmup_needed = df['EMA_200'].isna().sum() if 'EMA_200' in df.columns else 200
                warmup_ready = len(df) - warmup_needed
                print(f"   Warmup Period: {warmup_needed} candles")
                print(f"   Ready for Signals: {warmup_ready} candles")
                if warmup_ready < 100:
                    print(f"   ⚠️  WARNING: Only {warmup_ready} candles available after warmup!")
        
        return analysis
    
    def analyze_strategy_signals(self, df: pd.DataFrame, symbol: str) -> Dict:
        """Analyze signals from each strategy"""
        print(f"\n🎯 Strategy Signal Analysis for {symbol}")
        print("-" * 60)
        
        signal_analysis = {}
        
        try:
            for strategy_name, strategy_info in STRATEGY_CONFIG.items():
                strategy_func = strategy_info['function']
                weight = strategy_info['weight']
                
                # Generate signals
                long_signals, short_signals, exit_params = strategy_func(df.copy())
                
                long_count = long_signals.sum() if isinstance(long_signals, pd.Series) else 0
                short_count = short_signals.sum() if isinstance(short_signals, pd.Series) else 0
                
                signal_analysis[strategy_name] = {
                    'weight': weight,
                    'long_signals': long_count,
                    'short_signals': short_count,
                    'total_signals': long_count + short_count,
                    'exit_params': exit_params
                }
                
                status = "✅" if (long_count + short_count) > 0 else "❌"
                print(f"   {status} {strategy_name} (weight: {weight}):")
                print(f"      Long: {long_count}, Short: {short_count}, Total: {long_count + short_count}")
                print(f"      Exit Params: SL={exit_params.get('sl_multiplier', 'N/A')}, "
                      f"RR={exit_params.get('rr_ratio', 'N/A')}")
                
        except Exception as e:
            print(f"   ❌ Error analyzing strategies: {e}")
            import traceback
            traceback.print_exc()
        
        return signal_analysis
    
    def analyze_consensus(self, df: pd.DataFrame, signal_analysis: Dict, symbol: str) -> Dict:
        """Analyze consensus scoring"""
        print(f"\n🤝 Consensus Analysis for {symbol}")
        print("-" * 60)
        
        consensus_ratio = LIVE_TRADING_CONFIG.get('consensus_ratio', 0.6)
        print(f"   Consensus Threshold: {consensus_ratio}")
        
        try:
            # Simulate consensus scoring
            long_scores = pd.Series(0.0, index=df.index)
            short_scores = pd.Series(0.0, index=df.index)
            total_weight = sum([info['weight'] for info in STRATEGY_CONFIG.values()])
            
            for strategy_name, strategy_info in STRATEGY_CONFIG.items():
                strategy_func = strategy_info['function']
                weight = strategy_info['weight']
                
                long_signals, short_signals, _ = strategy_func(df.copy())
                
                long_scores += long_signals.astype(float) * weight
                short_scores += short_signals.astype(float) * weight
            
            required_score = total_weight * consensus_ratio
            long_above_threshold = (long_scores >= required_score).sum()
            short_above_threshold = (short_scores >= required_score).sum()
            
            print(f"   Total Strategy Weight: {total_weight}")
            print(f"   Required Score for Consensus: {required_score:.2f}")
            print(f"   Long Signals Above Threshold: {long_above_threshold}")
            print(f"   Short Signals Above Threshold: {short_above_threshold}")
            print(f"   Total Consensus Signals: {long_above_threshold + short_above_threshold}")
            
            if long_above_threshold + short_above_threshold == 0:
                print(f"\n   ⚠️  NO CONSENSUS SIGNALS GENERATED!")
                print(f"   Max Long Score Achieved: {long_scores.max():.3f}")
                print(f"   Max Short Score Achieved: {short_scores.max():.3f}")
                
                if max(long_scores.max(), short_scores.max()) < required_score:
                    print(f"   💡 ISSUE: Consensus threshold ({consensus_ratio}) is too high!")
                    print(f"   💡 SUGGESTION: Lower CONSENSUS_RATIO to {max(long_scores.max(), short_scores.max()) * 0.9:.2f}")
            
            return {
                'consensus_ratio': consensus_ratio,
                'long_signals': long_above_threshold,
                'short_signals': short_above_threshold,
                'max_long_score': long_scores.max(),
                'max_short_score': short_scores.max()
            }
            
        except Exception as e:
            print(f"   ❌ Error in consensus analysis: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def print_recommendations(self, all_analysis: Dict):
        """Print recommendations based on analysis"""
        print("\n" + "="*60)
        print("💡 RECOMMENDATIONS")
        print("="*60)
        
        recommendations = []
        
        # Check if any signals were generated
        total_signals = sum([
            analysis.get('consensus_analysis', {}).get('long_signals', 0) + 
            analysis.get('consensus_analysis', {}).get('short_signals', 0)
            for analysis in all_analysis.values()
        ])
        
        if total_signals == 0:
            recommendations.append(
                "❌ NO SIGNALS GENERATED ACROSS ALL SYMBOLS\n"
                "   Primary Issues to Address:"
            )
            
            # Check consensus ratio
            for symbol, analysis in all_analysis.items():
                consensus_data = analysis.get('consensus_analysis', {})
                if consensus_data:
                    max_score = max(
                        consensus_data.get('max_long_score', 0),
                        consensus_data.get('max_short_score', 0)
                    )
                    threshold_ratio = consensus_data.get('consensus_ratio', 0.6)
                    
                    if max_score < (sum(s['weight'] for s in STRATEGY_CONFIG.values()) * threshold_ratio):
                        recommendations.append(
                            f"\n1. LOWER `consensus_ratio` in config.py:\n"
                            f"   Current: {threshold_ratio}\n"
                            f"   Suggested: {max_score * 0.85:.2f}\n"
                            f"   (Set to 85% of highest score: {max_score:.3f})"
                        )
                        break
            
            # Check data quantity
            for symbol, analysis in all_analysis.items():
                data_quality = analysis.get('data_quality', {})
                if data_quality.get('total_candles', 0) < 500:
                    recommendations.append(
                        f"\n2. INCREASE DATA LIMIT:\n"
                        f"   Current: {self.limit} candles\n"
                        f"   Suggested: 2000-5000 candles for better backtesting"
                    )
                    break
            
            # Check strategy signals
            all_strategy_signals = []
            for symbol, analysis in all_analysis.items():
                signal_analysis = analysis.get('signal_analysis', {})
                for strategy, data in signal_analysis.items():
                    all_strategy_signals.append(data.get('total_signals', 0))
            
            if sum(all_strategy_signals) == 0:
                recommendations.append(
                    f"\n3. STRATEGY CONDITIONS TOO RESTRICTIVE:\n"
                    f"   No individual strategy is generating signals!\n"
                    f"   Action: Review and relax conditions in strategies.py"
                )
            
            recommendations.append(
                f"\n4. TEST WITH HIGH-VOLATILITY PERIODS:\n"
                f"   Current market conditions might be too stable\n"
                f"   Try testing during known volatile periods (e.g., 2021 bull run)"
            )
            
            recommendations.append(
                f"\n5. VERIFY INDICATOR CALCULATIONS:\n"
                f"   Run: python diagnostics.py\n"
                f"   Check if indicators are properly calculated"
            )
        else:
            recommendations.append(
                f"✅ SIGNALS ARE BEING GENERATED!\n"
                f"   Total signals across all symbols: {total_signals}\n"
                f"   Your bot configuration is working correctly."
            )
        
        for rec in recommendations:
            print(rec)
        
        print("\n" + "="*60)
    
    async def run_full_diagnostics(self, symbol_count: int = 5):
        """Run complete diagnostic analysis"""
        if not await self.initialize_exchange():
            return
        
        # Get symbols
        self.symbols = await self.get_top_symbols(symbol_count)
        
        if not self.symbols:
            print("❌ No symbols found. Exiting.")
            return
        
        all_analysis = {}
        
        # Analyze each symbol
        for symbol in self.symbols:
            print(f"\n{'='*60}")
            print(f"🔍 Analyzing {symbol}")
            print(f"{'='*60}")
            
            df = await self.fetch_and_prepare_data(symbol)
            
            if df is None or df.empty:
                continue
            
            analysis = {
                'data_quality': self.analyze_data_quality(df, symbol),
                'signal_analysis': self.analyze_strategy_signals(df.copy(), symbol),
                'consensus_analysis': self.analyze_consensus(df, 
                    self.analyze_strategy_signals(df, symbol), symbol)
            }
            
            all_analysis[symbol] = analysis
        
        # Print recommendations
        self.print_recommendations(all_analysis)
        
        print("\n✅ Diagnostics completed!")


async def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description="Scalper Bot Diagnostics Script")
    parser.add_argument("--start_date", type=str, default=None, help="Start date for analysis in YYYY-MM-DD format")
    parser.add_argument("--end_date", type=str, default=None, help="End date for analysis in YYYY-MM-DD format")
    parser.add_argument("--symbols", type=int, default=3, help="Number of top symbols to analyze")
    args = parser.parse_args()

    if args.start_date:
        print(f"Running diagnostics for period: {args.start_date} to {args.end_date or 'latest'}")

    diagnostics = ScalperDiagnostics(start_date=args.start_date, end_date=args.end_date)
    
    await diagnostics.run_full_diagnostics(symbol_count=args.symbols)


if __name__ == "__main__":
    print("Starting Scalper Bot Diagnostics...")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Diagnostics interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()