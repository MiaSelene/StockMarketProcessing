# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 11:57:48 2019

@author: User
"""
import requests
import json
import matplotlib.pyplot as plt
import numpy


class Trader:
    def __init__(self,equity,stocks):
        self.equity = equity
        self.stocks = stocks
        self.XB = []
        self.YB = []
        self.XS = []
        self.YS = []
        
        
    def Buy(self,price,cost,i):
        self.equity -= cost
        while price < self.equity:
            self.stocks += 1
            self.equity -= price
        self.XB.append(i)
        self.YB.append(price)
        

    def Sell(self,price,cost,i):
        self.equity -= cost
        while self.stocks > 0:
            self.stocks -= 1
            self.equity += price
        self.XS.append(i)
        self.YS.append(price)
    def NetWorth(self,Price):
        return self.equity + self.stocks * Price
    
    def Graph(self,hist):
        plt.subplot(2,2,4)
        plt.hist([S-B for B,S in zip(self.YB,self.YS)])
        plt.title("Decision Effectiveness")
        plt.subplot(2,2,1)
        plt.title("Buy/Sell Decisions")
        plt.scatter(self.XS,self.YS,s=100,c="g")
        plt.scatter(self.XB,self.YB,s=100,c="r")
        plt.plot([i for i in range(len(hist))],hist,"b-")
        plt.subplot(2,2,2)
        plt.title("Equity over Time")
        plt.plot(Graph)
        plt.plot([8000 for i in Graph])
        plt.subplot(2,2,3)
        plt.title("Fourier Noise Reduction")
        plt.plot(numpy.fft.ifft([0 if abs(x)<3000 else x for x in numpy.fft.rfft(Werte)]))
        
        
def Trend(List):
    return List[-1]-List[0]


def Var(List):
    avg=sum(List)/len(List)
    return sum([numpy.square(x-avg) for x in List])/len(List)


def normalize(List):
    normal=[]
    Prime=RelevantTrend(List)/len(List)
    for i in range(len(List)):
        normal.append(List[i]-Prime*i)
    return normal



def NEGmoddedOST(List):
    stop=int(len(List)/numpy.e)
    Estimate=min(List[:stop])
    avg=sum(List[:stop])/stop
    m=RelevantTrend(List[:stop])
    for i in range(stop,len(List)):
        Entry=List[i]
        Needed=avg+(Estimate-avg)*(1-(i-stop)/(len(List)-stop))*(1+m)
        if Entry<Needed:
            return Entry,i
    return Entry,i


def moddedOST(List):
    stop=int(len(List)/numpy.e)
    Estimate=max(List[:stop])
    avg=sum(List[:stop])/stop
    m=RelevantTrend(List[:stop])
    for i in range(stop,len(List)):
        Entry=List[i]
        Entry=List[i]
        Needed=avg+(Estimate-avg)*(1-(i-stop)/(len(List)-stop))*(1+m)
        if Entry>Needed:
            return Entry,i
    return Entry,i


def get_stocks_time_series(sign_list):
    stock_time_series=[]
    for sign in sign_list:
        json_data=requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={sign}&interval=1min&outputsize=full&apikey=SARLUC149FRWL21N")
        loaded=json.loads(json_data.content)
        keys = list(reversed(list(loaded["Time Series (Daily)"].keys())))
        stock_time_series.append([float(loaded["Time Series (Daily)"][key]["4. close"]) for key in keys])
        print(f"{sign} Data ranging from {keys[0]} to {keys[-1]}")
    return stock_time_series




        

    
    

def RelevantTrend(List):
    sig=numpy.sqrt(Var(List))
    m=Trend(List)
    if not m>2*sig or not m<-2*sig:
        return 0
    return m



XB=[]
YB=[]
XS=[]
YS=[]
TradePrice=6.95
i=0
Periode=400
Graph=[]
redPeriode=int(Periode/numpy.e)
Werte=get_stocks_time_series(['NTDOY'])[0]
Budda = Trader(8000,0)
while i<(len(Werte)-Periode):
    BuyPreis,BuyPunkt=NEGmoddedOST(Werte[i:i+Periode])
    i+=BuyPunkt
    Budda.Buy(Werte[i],TradePrice,i)
    Graph.append(Budda.NetWorth(Werte[i]))
    if i>(len(Werte)-Periode):
        continue
    SellPreis,SellPunkt=moddedOST(Werte[i:i+Periode])
    i+=SellPunkt
    Budda.Sell(Werte[i],TradePrice,i)
    Graph.append(Budda.NetWorth(Werte[i]))
    
 
calc = numpy.round((Budda.NetWorth(Werte[i])/8000.0), 3)
print(f"Factor {calc} after 20 years of Trading")

Budda.Graph(Werte)





