import numpy as np
import requests
import json
def get_stocks_time_series(sign_list):
    stock_time_series=[]
    for sign in sign_list:
        json_data=requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={sign}&interval=1min&outputsize=full&apikey=SARLUC149FRWL21N")
        loaded=json.loads(json_data.content)
        keys = list(reversed(list(loaded["Time Series (Daily)"].keys())))
        stock_time_series.append([float(loaded["Time Series (Daily)"][key]["4. close"]) for key in keys])
        print(f"{sign} Data ranging from {keys[0]} to {keys[-1]}")
    return stock_time_series

class Trader:
    def __init__(self,equity,stocks):
        self.equity = equity
        self.stocks = stocks


    def Buy(self,price,cost):
        self.equity -= cost
        while price < self.equity:
            self.stocks += 1
            self.equity -= price


    def Sell(self,price,cost):
        self.equity -= cost
        while self.stocks > 0:
            self.stocks -= 1
            self.equity += price

    def NetWorth(self,Price):
        return self.equity + self.stocks * Price


def time_series(batch):
    pred = batch[-1]
    mue = sum(batch)/len(batch)
    variance = sum([(b-mue)**2 for b in batch])/len(batch)
    dP = max(0,batch[-1]-batch[-2] -variance) if batch[-1]-batch[-2]>0 else min(0,batch[-1]-batch[-2] +variance)
    A=1
    i=0
    while i<len(batch):
        pred += dP
        APrime = 1/2 - np.sqrt(dP*A + 1/4)
        dP = (APrime**2 - APrime)/A
        A+= APrime
        i +=1
    return pred


if __name__ == "__main__":
    data = get_stocks_time_series(["DAX"])[0]
    Gunz = Trader(10000,0)
    batch_size = 100
    i = 620
    while i<len(data):
        print((time_series(data[i:i+batch_size])-data[i+batch_size])**2)
        i+=1
