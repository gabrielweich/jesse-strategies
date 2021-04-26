from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils


class IFR2(Strategy):
    @property
    def ichimoku(self):
        return ta.ichimoku_cloud(self.candles)

    @property
    def rsi(self):
        return ta.rsi(self.candles, period=2)

    @property
    def trend_mode(self):
        return ta.ht_trendmode(self.candles)

    @property
    def ichimoku(self):
        return ta.ichimoku_cloud(self.candles, conversion_line_period=20, base_line_period=30, lagging_line_period=120, displacement=60)

    def filter_trend_ichimoku(self):
        return self.close > self.ichimoku.span_a and self.close > self.ichimoku.span_b

    def filter_trend_mode(self):
        return self.trend_mode == 1

    def filters(self):
        return [self.filter_trend_ichimoku, self.filter_trend_mode]

    def should_long(self) -> bool:
        return self.rsi < 10

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