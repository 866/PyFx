#TODO: MUST BE TESTED
#order position
BUY = 1
SELL = -1
#order state
ACTIVE = 0
FORCED_CLOSE = 1
TP_REACHED = 2
SL_REACHED = 3


class Order(object):
    """ Representation of a financial order """
    def __init__(self, open_price, factor, order_position, open_date, stop_loss=None, take_profit=None):
        """
        :param open_price: price at which order is executed
        :param factor: Lot analogue
        :param order_position: BUY OR SELL type
        :param stop_loss: Stop loss price
        :param take_profit: Take profit price
        :return: nothing
        """
        self.open_price = open_price
        self.factor = factor
        self.order_position = order_position
        self.open_date = open_date
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.state = ACTIVE
        self.result = None
        self.close_date = None

    def perform_step(self, candle):
        """
        :param candle: current candle
        :return: <self.state>, <order result>
        """
        if self.state is not ACTIVE:
            return self.state, self.result
        if self.order_position is BUY:
            return self._calc_buy(candle)
        else:
            return self._calc_sell(candle)

    def close_order(self, close_price, close_date):
        self.state = FORCED_CLOSE
        self.result = close_price - self.open_price
        self.close_date = close_date
        return self.result

    def print_information(self):
        FORCED_CLOSE

    def _calc_buy(self, candle):
        #   could be ambivalent situation when
        #   TP and SL are reached in one day
        #   but we choose loss
        if (self.take_profit is not None) and (candle.High >= self.take_profit):
            self.result = (self.take_profit-self.open_price)*self.factor
            self.state = TP_REACHED
        if (self.stop_loss is not None) and (candle.Low <= self.stop_loss):
            self.result = (self.stop_loss-self.open_price)*self.factor
            self.state = SL_REACHED
        return self.state, self.result

    def _calc_sell(self, candle):
        #   could be ambivalent situation when
        #   TP and SL are reached in one day
        #   but we choose loss
        if (self.take_profit is not None) and (candle.Low <= self.take_profit):
            self.result = (self.open_price-self.take_profit)*self.factor
            self.state = TP_REACHED
        if (self.stop_loss is not None) and (candle.High >= self.stop_loss):
            self.result = (self.open_price-self.stop_loss)*self.factor
            self.state = SL_REACHED
        return self.state, self.result

