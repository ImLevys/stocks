import re
import pandas as pd
from datetime import date, timedelta
import yahoo
import operator


class List:

    def __init__(self):
        self.stock_list = open('stock_lists.dat', 'r')
        self.stock_list = self.stock_list.read()
        self.block_list = open('block_list.dat', 'r')
        self.block_list = self.block_list.read()
        self.otc_list = open('OTC.DAT', 'r')
        self.otc_list = self.otc_list.read()
        self.reddit_list = []
        self.result = {}
        self.today = date.today()
        self.yesterday = date.today() - timedelta(days=1)

    def match_stock(self):
        file = open('submission.txt', 'r')
        regex = r"\b([A-Z]){1,5}\b"
        file = file.read()
        matches = re.finditer(regex, file)
        for match in matches:
            if match[0] in self.stock_list:
                if match[0] not in self.block_list:
                    self.reddit_list.append(match[0])
            else:
                if match[0] in self.otc_list:
                    if match[0] not in self.block_list:
                        self.reddit_list.append(match[0])

    def count_stocks(self):
        for i in self.reddit_list:
            count = self.reddit_list.count(i)
            self.result.update({i: count})
        self.result = dict(sorted(self.result.items(), key=operator.itemgetter(1), reverse=True))
        print(self.result)

    def data_frame(self, subreddit):
        df = pd.DataFrame(list(self.result.items()), columns=['Ticker', 'Mentions'])
        df.to_csv(r'./' + subreddit + '/' + str(self.today) + '.csv', index=None)

    def delta(self, subreddit):
        today_csv = pd.read_csv('./' + subreddit + '/' + str(self.today) + '.csv')
        yesterday_csv = pd.read_csv('./' + subreddit + '/' + str(self.yesterday) + '.csv')
        dict_today = today_csv.set_index('Ticker')['Mentions'].to_dict()
        dict_yesterday = yesterday_csv.set_index('Ticker')['Mentions'].to_dict()
        for k, v in dict_today.items():
            if k in dict_yesterday.keys():
                delta = v - dict_yesterday[k]
                if delta > 0:
                    print(f"{k} Has {delta} New Posts From Yesterday")
                if delta == 0:
                    print(f"{k} {dict_today[k]} Has nothing new ")
                if delta < 0:
                    print(f"{k} Has {delta} Posts")
            elif k not in dict_yesterday.keys():
                print(f"{k} Has {dict_today[k]} New Posts ")
            yahoo.yahoo(stock=k)

x = List()
x.match_stock()
x.count_stocks()
x.data_frame('pennystocks')
x.delta('pennystocks')
