from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
import numpy as np
from jesse import utils


"""
XMR-USDT: 6h
"""


class DaveLandry(Strategy):
    @property
    def trend_ma(self):
        return ta.sma(self.candles, period=20)

    def filter_trend(self):
        return self.close > self.trend_ma

    def filters(self):
        return [self.filter_trend]

    def should_long(self) -> bool:
        return (
            self.low < self.candles[-2:, 4][-2] and self.low < self.candles[-3:, 4][-3]
        )

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
        if (
            self.close > self.candles[-2:, 3][-2]
            and self.close > self.candles[-3:, 3][-3]
        ):
            self.liquidate()