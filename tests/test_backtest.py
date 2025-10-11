import pytest
from decimal import Decimal

# Add project root to path to allow imports from sibling directories
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backtest import apply_slippage_and_fees, compute_position_size

# Mock configurations
SLIPPAGE_CONFIG = {"pct": 0.001, "fixed": 0.5} # 0.1% + $0.5
FEE_CONFIG = {"taker": 0.0007, "maker": 0.0002}
CONTRACT_SPEC = {"contract_size": 0.001, "point_value": 1.0}

@pytest.mark.parametrize("price, direction, expected_price", [
    (50000, 'LONG', 50000 * (1 + 0.001) + 0.5), # 50000 + 50 + 0.5 = 50050.5
    (50000, 'SHORT', 50000 * (1 - 0.001) - 0.5), # 50000 - 50 - 0.5 = 49949.5
])
def test_apply_slippage(price, direction, expected_price):
    """Tests that slippage is applied correctly."""
    exec_price, _ = apply_slippage_and_fees(price, direction, SLIPPAGE_CONFIG, FEE_CONFIG)
    assert exec_price == pytest.approx(expected_price)

@pytest.mark.parametrize("order_type, expected_fee_rate", [
    ('taker', 0.0007),
    ('maker', 0.0002),
])
def test_apply_fees(order_type, expected_fee_rate):
    """Tests that the correct fee rate is returned."""
    _, fee_rate = apply_slippage_and_fees(50000, 'LONG', SLIPPAGE_CONFIG, FEE_CONFIG, order_type)
    assert fee_rate == expected_fee_rate


def test_compute_position_size_normal():
    """Tests normal position size calculation."""
    balance = 10000
    risk_per_trade = 0.01 # Risk $100
    entry_price = 50000
    stop_price = 49800 # $200 stop distance
    leverage = 10

    # Risk per contract = stop_distance * point_value * contract_size
    # Risk per contract = 200 * 1.0 * 0.001 = $0.2
    # Contracts = risk_amount / risk_per_contract = 100 / 0.2 = 500
    # Notional = 500 * 50000 * 0.001 = $25,000
    # Margin = 25000 / 10 = $2,500
    # Since 2500 < 10000, this is valid.
    
    contracts, margin, notional = compute_position_size(
        balance, risk_per_trade, entry_price, stop_price, leverage, CONTRACT_SPEC
    )
    
    assert contracts == 500.0
    assert margin == pytest.approx(2500.0)
    assert notional == pytest.approx(25000.0)

def test_compute_position_size_insufficient_margin():
    """Tests case where risk-based size exceeds available margin."""
    balance = 1000
    risk_per_trade = 0.01 # Risk $10
    entry_price = 50000
    stop_price = 49980 # $20 stop distance
    leverage = 10

    # Risk per contract = 20 * 1.0 * 0.001 = $0.02
    # Contracts = 10 / 0.02 = 500
    # Notional = 500 * 50000 * 0.001 = $25,000
    # Margin = 25000 / 10 = $2,500
    # Since 2500 > 1000, this is invalid.
    
    contracts, margin, notional = compute_position_size(
        balance, risk_per_trade, entry_price, stop_price, leverage, CONTRACT_SPEC
    )
    
    assert contracts == 0
    assert margin == 0
    assert notional == 0

def test_compute_position_size_zero_stop_distance():
    """Tests edge case with zero stop distance to prevent division by zero."""
    contracts, margin, notional = compute_position_size(
        10000, 0.01, 50000, 50000, 10, CONTRACT_SPEC
    )
    assert contracts == 0
    assert margin == 0
    assert notional == 0