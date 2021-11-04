from ib_insync import *

'''ib = IB()
ib.connect(port=4002)
a = Option('SPX', '20211101', 4465, 'C', 'SMART')
ib.qualifyContracts(a)
d = ib.reqMktData(a, '221')
ib.sleep(5)'''

class Trade:
    def __init__(self):
        self.ib = IB()
        self.ib.connect(port=4001)

    def get_spx_first_candle(self):
        spx = Stock('SPX', 'CBOE', 'USD')
        self.ib.qualifyContracts(spx)
        data = self.ib.reqHistoricalData(spx,
                                    endDateTime='',
                                    durationStr='480',
                                    barSizeSetting='15 mins',
                                    whatToShow='TRADES',
                                    useRTH=True,
                                    formatDate=1)
        # list(filter(lambda x: x.date == datetime.datetime(2021, 11, 3, 21, 45), data))
        #[BarData(date=datetime.datetime(2021, 11, 3, 21, 30), open=4630.65, high=4630.65, low=4621.74, close=4625.57, volume=0.0, average=0.0, barCount=875), BarData(date=datetime.datetime(2021, 11, 3, 21, 45), open=4626.04, high=4628.76, low=4624.72, close=4627.52, volume=0.0, average=0.0, barCount=864), BarData(date=datetime.datetime(2021, 11, 3, 22, 0), open=4627.4, high=4628.46, low=4621.18, close=4623.32, volume=0.0, average=0.0, barCount=627)]
        max_price = data1.high
        min_price = data1.low
        print(max_price, min_price)

    def get_option_basket(self, high_strike, low_strike):
        #strike date =
        low = Option('SPX', '20211103', low_strike, 'P', 'SMART')
        self.ib.qualifyContracts(low)

        high = Option('SPX', '20211103', high_strike, 'P', 'SMART')
        self.ib.qualifyContracts(high)

        contract = Contract()
        contract.symbol = low.symbol
        contract.secType = 'BAG'
        contract.currency = low.currency
        contract.exchange = high.exchange

        leg1 = ComboLeg()
        leg1.conId = low.conId
        leg1.ratio = 1
        leg1.action = 'BUY'
        leg1.exchange = low.exchange

        leg2 = ComboLeg()
        leg2.conId = high.conId
        leg2.ratio = 1
        leg2.action = 'SELL'
        leg2.exchange = high.exchange

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)

        d = self.ib.reqMktData(contract) #, '221'
        #self.ib.sleep(1)
        #d.marketPrice()