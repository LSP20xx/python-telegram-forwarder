import re

def filter_and_extract_orders(messages):
    orders = []

    # Simplified regular expression to capture the main components of the order
    order_pattern = re.compile(
        r'#(?P<ticker>[A-Z]+\/USDT).*?-\s*(?P<entry_price>\d+(\.\d+)?).*?Targets:\s*(?P<targets>[\d\-]+).*?Stop.*?-\s*(?P<stop_loss>\d+(\.\d+)?)',
        re.IGNORECASE
    )

    for message in messages:
        match = order_pattern.search(message)
        if match:
            order_info = match.groupdict()
            order_info['targets'] = order_info['targets'].split('-')
            orders.append(order_info)
        else:
            print(f"No match found for message: {message}")
    
    return orders


def save_extracted_orders(file_path, orders):
    if orders:
        with open(file_path, 'w') as file:
            for order in orders:
                file.write(f"Ticker: {order['ticker']}\n")
                file.write(f"Entry Price: {order['entry_price']}\n")
                file.write(f"Targets: {', '.join(order['targets'])}\n")
                file.write(f"Stop Loss: {order['stop_loss']}\n")
                file.write(f"{'-'*40}\n")
        print(f"Orders saved to {file_path}")
    else:
        print("No orders to save.")


# Messages list
messages = [
    "Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #SUI/USDT Long/Buy - 8530 Targets: 8710 Leverage - 10x Stop Loss - 8180",
    "Premium Crypto Group, [9/8/24 10:08] #REZ/USDT at (Binance, ByBit, KuCoin, OKX) Buy - 510 Selling Targets – 515-535-565-590 Stop around – 430",
    "Premium Crypto Group, [9/8/24 10:12] #COMBO/USDT Buy - 4100 Selling Targets - 4141-4305-4510-4715 Stop Suggested – 3480",
    "Premium Crypto Group, [9/8/24 11:13] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #TON/USDT Long/Buy - 6.6000 Targets: 6.7320 Leverage - 10x Stop Loss - 6.3360",
    "Premium Crypto Group, [9/8/24 14:16] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi Long/Buy #TIA/USDT Enter Point - 5.7700 Targets: 5.885 Leverage - 10x Stop Loss - 5.530",
    "Premium Crypto Group, [9/8/24 15:58] #QKC/USDT at (Binance, ByBit, KuCoin, Bitget) Buy - 10300 Selling Targets - 10500-10950-11450-12000 Stop around – 8800",
    "Premium Crypto Group, [9/8/24 16:01] Binance Futures, OKX, Gate.io, Bitget, BybitUSDT, Kucoin #TOKEN/USDT Long/Buy - 7400 Targets: 7550 Leverage - 10x Stop Loss - 7100",
    "Premium Crypto Group, [9/8/24 16:06] #ZEC/USDT at (Binance, ByBit, KuCoin, OKX) Buy - 40.00 Selling Targets - 40.40-42.00-44.00-46.00 Stop below – 34.00",
    "Premium Crypto Group, [9/8/24 16:06] #GNO/USDT Buy - 166 Selling Targets - 168-175-183-191 Stop around – 140",
    "Premium Crypto Group, [9/8/24 16:27] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #TON/USDT Long/Buy - 6.5500 Targets: 6.6810 Leverage - 10x Stop Loss - 6.2880",
    "Premium Crypto Group, [9/8/24 17:16] #ERN/USDT (Binance, ByBit, KuCoin, Bitget) Buy - 2.240 Targets – 2.265 - 2.355 - 2.465 - 2.580 Stop around – 1.900",
    "Premium Crypto Group, [9/8/24 17:18] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #BIGTIME/USDT Long/Buy - 875 Targets: 895 Leverage - 10x Stop Loss - 840",
    "Premium Crypto Group, [10/8/24 4:38] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi Long/Buy #TIA/USDT Enter Point - 5.7700 Targets: 5.885 Leverage - 10x Stop Loss - 5.530",
    "Premium Crypto Group, [10/8/24 7:38] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #SUI/USDT Long/Buy - 8820 Targets: 9000 Leverage - 10x Stop Loss - 8460",
    "Premium Crypto Group, [10/8/24 8:12] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #BIGTIME/USDT Long/Buy - 930 Targets: 950 Leverage - 10x Stop Loss - 890",
    "Premium Crypto Group, [10/8/24 8:15] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi Long/Buy #TIA/USDT Enter Point - 5.7800 Targets: 5.9000 Leverage - 10x Stop Loss - 5.5480",
    "Premium Crypto Group, [10/8/24 8:20] #CVP/USDT at (Binance, ByBit, KuCoin, OKX) Buy - 3600 Selling Targets - 3620-3640-3655-3680 Stop around – 3450",
    "Premium Crypto Group, [10/8/24 10:12] #CTXC/USDT at (Binance, ByBit, KuCoin, OKX, Bitget) Buy - 1860 Selling Targets - 1890-1955-2050-2140 Stop at – 1500",
    "Premium Crypto Group, [10/8/24 10:35] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #ZETA/USDT Long/Buy - 6245 Targets: 6370 Leverage - 10x Stop Loss - 5995",
    "Premium Crypto Group, [10/8/24 11:30] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #INJ/USDT Long/Buy - 19.370 Targets: 19.760 Leverage - 10x Stop Loss - 18.590",
    "Premium Crypto Group, [11/8/24 5:00] #T/USDT at (Binance, ByBit, KuCoin, OKX) Buy - 2400 Selling Targets - 2424-2520-2640-2760 Stop loss – 2040",
    "Premium Crypto Group, [11/8/24 5:02] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #T/USDT Long/Buy - 2400 Targets: 2450 Leverage - 10x Stop Loss - 2300",
    "Premium Crypto Group, [11/8/24 5:03] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #PENDLE/USDT Long/Buy - 2.8500 Targets: 2.9080 Leverage - 10x Stop Loss - 2.7360",
    "Premium Crypto Group, [11/8/24 6:43] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi Long/Buy #DAR/USDT Entry Point - 1415 Targets: 1445 Leverage - 10x Stop Loss - 1355",
    "Premium Crypto Group, [12/8/24 5:03] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #ASTR/USDT Long/Buy - 5855 Targets: 6000 Leverage - 10x Stop Loss - 5620",
    "Premium Crypto Group, [12/8/24 5:04] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #ZEC/USDT Long/Buy - 41.45 Targets: 42.300 Leverage - 10x Stop Loss - 39.790",
    "Premium Crypto Group, [12/8/24 5:06] #T/USDT at (Binance, ByBit, KuCoin, OKX) Buy - 2400 Selling Targets - 2424-2520-2640-2760 Stop loss – 2040",
    "Premium Crypto Group, [12/8/24 5:12] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi Long/Buy #RENDER/USDT Entry Point - 8.610 Targets: 8.790 Leverage - 10x Stop Loss - 8.265",
    "Premium Crypto Group, [12/8/24 5:35] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #CYBER/USDT Long/Buy - 2.985 Targets: 3.050 Leverage - 10x Stop Loss - 2.860",
    "Premium Crypto Group, [12/8/24 5:38] #GLM/USDT at (Binance, ByBit Spot, Huobi.pro, OKX) Buy - 3200 Selling Targets - 3235-3360-3520-3680 Stop Suggested – 2700",
    "Premium Crypto Group, [12/8/24 6:31] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #SUI/USDT Long/Buy - 9590 Targets: 9785 Leverage - 10x Stop Loss - 9200",
    "Premium Crypto Group, [12/8/24 7:43] Binance Futures, OKX, Deribit, BitGET, BybitUSDT, KuCoin, Huobi #LDO/USDT Long/Buy - 1.095 Targets: 1.117 Leverage - 10x Stop Loss - 1.050"
]

# Extract and save orders
orders = filter_and_extract_orders(messages)

save_extracted_orders('extracted_orders.txt', orders)
print("Total amount of orders: ",len(orders))
print("Order details extracted and saved successfully.")
