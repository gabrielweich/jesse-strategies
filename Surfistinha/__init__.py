from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils


class Surfistinha(Strategy):
    @property
    def bb(self):
        # Bollinger bands using default parameters and hl2 as source
        return ta.bollinger_bands(self.candles, source_type="hl2")

    @property
    def ichimoku(self):
        return ta.ichimoku_cloud(self.candles)

    def filter_trend(self):
        # Only opens a long position when close is above ichimoku cloud
        return self.close > self.ichimoku.span_a and self.close > self.ichimoku.span_b

    def filters(self):
        return [self.filter_trend]

    def should_long(self) -> bool:
        # Go long if candle closes above upperband
        return self.close > self.bb[0]

    def should_short(self) -> bool:
        return False

    def should_cancel(self) -> bool:
        return True

    def go_long(self):
        # Open long position using entire balance
        qty = utils.size_to_qty(self.capital, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price

    def go_short(self):
        pass

    def update_position(self):
        # Close the position when candle closes below middleband
        if self.close < self.bb[1]:
            self.liquidate()