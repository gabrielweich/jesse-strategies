"""
Larry Willliams RSI4 Strategy
Reference: - High Probability ETF trading pg.23
"""

from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class RSI4(Strategy):
    def __init__(self):
        super().__init__()
        self.vars["slow_sma_period"] = 200
        self.vars["rsi_period"] = 4
        self.vars["rsi_exit_threshold"] = 55
        self.vars["rsi_os_threshold"] = 25

    @property
    def slow_sma(self):
        return ta.sma(self.candles, self.vars["slow_sma_period"])

    @property
    def rsi(self):
        return ta.rsi(self.candles, self.vars["rsi_period"])

    def should_long(self) -> bool:
        return self.price > self.slow_sma and self.rsi <= self.vars["rsi_os_threshold"]

    def should_short(self) -> bool:
        return False

    def should_cancel(self) -> bool:
        return False

    def go_long(self):
        qty = utils.size_to_qty(self.capital, self.price, fee_rate=self.fee_rate)

        self.buy = qty, self.price

    def go_short(self):
        pass

    def update_position(self):
        if self.rsi >= self.vars["rsi_exit_threshold"]:
            self.liquidate()