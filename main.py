from tradingview_ta import TA_Handler, Interval
import asyncio

data_eth = TA_Handler(
    symbol="ETHUSDTPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)
data_btc = TA_Handler(
    symbol="BTCUSDTPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

async def parse():
    hour_movements_percent = []
    minute = 0
    while True:
        print("\n", "minute:", minute )
        minute += 1
        if (minute == 1):
            price_prev_eth = (data_eth.get_analysis().indicators["close"])
            price_prev_btc = (data_btc.get_analysis().indicators["close"])
            print("price_eth:", price_prev_eth)
            print("price_btc:", price_prev_btc)
        else:
            price_eth = (data_eth.get_analysis().indicators["close"])
            price_btc = (data_btc.get_analysis().indicators["close"])
            change_eth_percent = ((price_eth - price_prev_eth)/price_prev_eth) * 100
            change_btc_percent = ((price_btc - price_prev_btc)/price_prev_btc) * 100
            price_prev_eth = price_eth
            price_prev_btc = price_btc
            price_movement_eth_percent = change_eth_percent - change_btc_percent
            hour_movements_percent.append(price_movement_eth_percent)
            if (len(hour_movements_percent) > 60):
                hour_movements_percent.pop(0)
            hour_change_percent = sum(hour_movements_percent)
            print("price_eth:", price_eth)
            print("price_btc:", price_btc)
            print("change_eth_percent:", change_eth_percent)
            print("change_btc_percent:", change_btc_percent)
            print("price_movement_eth_percent:", price_movement_eth_percent)
            print("hour_movements_percent:", hour_movements_percent)
            print("hour_change_percent:", hour_change_percent)
            if (abs(hour_change_percent) >= 1):
                print("Цена изменилась более чем на один процент за последний час")
        await asyncio.sleep(60)

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(parse())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()
