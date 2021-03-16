import yfinance as yf
import pandas as pd
import json


def del_null(ticker_data):
    for k, v in ticker_data.items():
        if v is None:
            ticker_data[k] = 'N/A'
    with open('stock.json', 'w') as info:
        json.dump(ticker_data, info)
    info.close()


def validation_precentage(param):
    if param != 'N/A':
        return "{:.0%}".format(param)


def validation_number(param):
    if param != 'N/A':
        return "{:,}".format(param)


def yahoo(stock):
    try:
        stock = yf.Ticker(stock)
        ticker_data = stock.info
        del_null(ticker_data)
        stock_dict = {
            'Symbol': ticker_data['symbol'],
            'Sector': ticker_data['sector'],
            'Price': validation_number(ticker_data['open']),
            'Market Cap': validation_number(ticker_data['marketCap']),
            'Shares Outstanding': validation_number(ticker_data['sharesOutstanding']),
            'Shares On Short': validation_number(ticker_data['sharesShort']),
            'Institutions Precentage': validation_precentage(ticker_data['heldPercentInstitutions']),
            'Profit Margin Precentage': validation_precentage(ticker_data['profitMargins']),
            'Volume Avg': validation_number(ticker_data['averageVolume']),
            '10 Days Volume': validation_number(ticker_data['averageVolume10days']),
            '52 Week Change Precentage': validation_precentage(ticker_data['52WeekChange'])
        }
        df = pd.DataFrame(stock_dict.items(), index=None, columns=['Info', 'Stock'])
        print(df + '\n')

    except:
        print("Couldn't Show Any Info From Yahoo")
        pass
