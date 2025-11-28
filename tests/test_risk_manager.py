import pytest
from binonrown.bot.risk_manager import RiskManager

def test_max_daily_trades():
    rm = RiskManager(max_daily_trades=2, stop_loss_pct=0.01)
    
    # First trade
    assert rm.check_trade_allowed() == True
    rm.record_trade()
    
    # Second trade
    assert rm.check_trade_allowed() == True
    rm.record_trade()
    
    # Third trade (should be blocked)
    assert rm.check_trade_allowed() == False

def test_stop_loss_calculation():
    rm = RiskManager(max_daily_trades=10, stop_loss_pct=0.05)
    
    entry_price = 100
    expected_sl_long = 95
    expected_sl_short = 105
    
    assert rm.calculate_stop_loss(entry_price, 'buy') == expected_sl_long
    assert rm.calculate_stop_loss(entry_price, 'sell') == expected_sl_short
