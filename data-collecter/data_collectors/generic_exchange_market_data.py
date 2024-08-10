import asyncio
from .base_collector import BaseCollector


class GenericExchangeMarketData(BaseCollector):
    def __init__(self, exchange, exchange_name, symbol, producer, topics):
        super().__init__(symbol, producer, topics)
        self.exchange = exchange
        self.exchange_name = exchange_name
        self.is_running = False

    async def start(self):
        self.is_running = True
        tasks = [
            self.collect_trades(),
            self.collect_orderbook(),
            self.collect_ohlcv()
        ]
        await asyncio.gather(*tasks)

    async def collect_trades(self):
        while self.is_running:
            try:
                trades = await self.exchange.watch_trades(self.symbol)
                for trade in trades:
                    data = {
                        'exchange': self.exchange_name,
                        'symbol': self.symbol,
                        'type': 'trade',
                        'data': trade
                    }
                    self.producer.send(self.topics['trade'], data)
            except Exception as e:
                print(f"Error watching trades for {self.exchange_name} {self.symbol}: {e}")
                await asyncio.sleep(5)

    async def collect_orderbook(self):
        while self.is_running:
            try:
                orderbook = await self.exchange.watch_order_book(self.symbol)
                data = {
                    'exchange': self.exchange_name,
                    'symbol': self.symbol,
                    'type': 'orderbook',
                    'data': orderbook
                }
                self.producer.send(self.topics['orderbook'], data)
            except Exception as e:
                print(f"Error watching orderbook for {self.exchange_name} {self.symbol}: {e}")
                await asyncio.sleep(5)

    async def collect_ohlcv(self):
        while self.is_running:
            try:
                ohlcv = await self.exchange.watch_ohlcv(self.symbol, '1m')
                data = {
                    'exchange': self.exchange_name,
                    'symbol': self.symbol,
                    'type': 'ohlcv',
                    'data': ohlcv
                }
                self.producer.send(self.topics['ohlcv'], data)
            except Exception as e:
                print(f"Error watching OHLCV for {self.exchange_name} {self.symbol}: {e}")
                await asyncio.sleep(5)

    async def stop(self):
        self.is_running = False