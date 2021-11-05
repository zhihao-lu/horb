from ib_insync import *
import datetime
import math

'''ib = IB()
ib.connect(port=4002)
a = Option('SPX', '20211101', 4465, 'C', 'SMART')
ib.qualifyContracts(a)
d = ib.reqMktData(a, '221')
ib.sleep(5)'''


class Trade:
    def __init__(self, port=4001):
        self.ib = IB()
        self.ib.connect(port=port)
        self.spx = Index('SPX', 'CBOE', 'USD')
        self.ib.qualifyContracts(self.spx)

    def get_spx_first_candle(self):
        data = self.ib.reqHistoricalData(self.spx,
                                         endDateTime='',
                                         durationStr='960 S',
                                         barSizeSetting='15 mins',
                                         whatToShow='TRADES',
                                         useRTH=True,
                                         formatDate=1)
        first_candle = list(filter(lambda x: x.date.minute == 30 and x.date.hour == 21, data))[0]
        max_price = first_candle.high
        min_price = first_candle.low
        return max_price, min_price

    def get_option_basket(self, short_strike, long_strike, p_c):
        strike_date = datetime.datetime.now().strftime('%Y%m%d')
        long = Option('SPX', strike_date, long_strike, p_c, 'SMART')
        self.ib.qualifyContracts(long)

        short = Option('SPX', strike_date, short_strike, p_c, 'SMART')
        self.ib.qualifyContracts(short)

        contract = Contract()
        contract.symbol = long.symbol
        contract.secType = 'BAG'
        contract.currency = long.currency
        contract.exchange = long.exchange

        leg1 = ComboLeg()
        leg1.conId = long.conId
        leg1.ratio = 1
        leg1.action = 'BUY'
        leg1.exchange = long.exchange

        leg2 = ComboLeg()
        leg2.conId = short.conId
        leg2.ratio = 1
        leg2.action = 'SELL'
        leg2.exchange = short.exchange

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)

        return contract
        # d = self.ib.reqMktData(contract)  # , '221'
        # self.ib.sleep(1)
        # d.marketPrice()

    def create_order(self, max_price, min_price):
        # if spx crosses high price in range
        bull_price_condition = PriceCondition(
            price=max_price,
            conId=self.spx.conId,
            exch=self.spx.exchange
        )

        bull_short_strike = (min_price//5)*5
        bull_long_strike = bull_short_strike - 5

        bull_contract = self.get_option_basket(bull_short_strike, bull_long_strike, 'P')


        # if spx crosses low price in range
        bull_price_condition = PriceCondition(
            price=min_price,
            conId=self.spx.conId,
            exch=self.spx.exchange
        )

        bear_short_strike = (math.ceil(max_price/5))*5
        bear_long_strike = bull_short_strike + 5

        bear_contract = self.get_option_basket(bear_short_strike, bear_long_strike, 'C')



        # append price condition to order
        # wrap it in bracket to take profit
        # put each bracket in oca to make sure each is ok
        return bull_contract, bear_contract

