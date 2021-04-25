from jesse.indicators.chande import chande
from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils


class MongeYokohama(Strategy):
    def __init__(self):
        super().__init__()
        self.candle = 0


    @property
    def ema_low(self):
        return ta.ema(self.candles, period=5, source_type="low")

    @property
    def ema_high(self):
        return ta.ema(self.candles, period=7, source_type="high")


    def should_long(self) -> bool:
        return self.close < self.ema_low/1.02

    def should_short(self) -> bool:
        return False

    def should_cancel(self) -> bool:
        return True

    def go_long(self):
        self.candle = 1
        qty = utils.size_to_qty(self.capital, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price

    def go_short(self):
        pass

    def update_position(self):
        if self.close > self.ema_high:
            self.liquidate()
        elif self.candle >= 2 and self.close > self.position.entry_price:
            self.liquidate()
        self.candle += 1