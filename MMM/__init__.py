from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

"""
Currencies: ETH, BTC, BNB, ADA
Timeframe: 1h
"""

class MMM(Strategy):
    @property
    def ma_high(self):
        return ta.sma(self.candles, period=3, source_type="high")
    
    @property
    def ma_low(self):
        return ta.sma(self.candles, period=3, source_type="low")

    @property
    def ma_trend(self):
        return ta.sma(self.candles, period=30, source_type="close")

    def filter_trend(self):
        return self.close > self.ma_trend

    def filters(self):
        return [self.filter_trend]

    def should_long(self) -> bool:
        return self.close < self.ma_low

    def should_short(self) -> bool:
        return False

    def should_cancel(self) -> bool:
        return True

    def go_long(self):
        qty = utils.size_to_qty(self.capital, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price

    def go_short(self):
        pass

    def update_position(self):
        if self.close > self.ma_high:
            self.liquidate()