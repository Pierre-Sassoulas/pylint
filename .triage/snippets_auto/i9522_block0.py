I got the message:
Using global for 'ticker' but no assignment is done

for the code:
---
def remove_ticker_from_list(stock_index):
    global ticker
    ticker[stock_index]="NULL_STOCK"
