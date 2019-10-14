# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 11:57:48 2019

@author: User
"""
import requests
import json
import matplotlib.pyplot as plt
import numpy
from typing import List

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
def get_stocks_time_series(sign_list=list):
    stock_time_series=[]
    for sign in sign_list:
        json_data=requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={sign}&interval=1min&outputsize=full&apikey=SARLUC149FRWL21N")
        loaded=json.loads(json_data.content)
        keys = list(reversed(list(loaded["Time Series (Daily)"].keys())))
        stock_time_series.append([float(loaded["Time Series (Daily)"][key]["4. close"]) for key in keys])
        print(f"{sign} Data ranging from {keys[0]} to {keys[-1]}")
    return stock_time_series



def Buy(Preis,Gebühren,i):
    global Guthaben
    global Aktien
    global XB
    global YB
    Guthaben-=Gebühren
    while Preis<Guthaben:
        Aktien+=1
        Guthaben-=Preis
    XB.append(i)
    YB.append(Werte[i])
        
def Sell(Preis,Gebühren,i):
    global Guthaben
    global Aktien
    global XS
    global YS
    Guthaben-=Gebühren
    while Aktien>0:
        Aktien-=1
        Guthaben+=Preis
    XS.append(i)
    YS.append(Werte[i])
    
    

def RelevantTrend(List):
    sig=numpy.sqrt(Var(List))
    m=Trend(List)
    
    if not m>2*sig or not m<-2*sig:
        return 0
    
    return m
    
    
    if m>2*sig:
        return m
    elif m<-2*sig:
        return m
    else:
        return 0
    
    
    if a == "apple":
        return "this is fruit"
    elif a == "bannana":
        return "this is fruit"
    else:
        return "this is not a fruit"
    


XB=[]
YB=[]
XS=[]
YS=[]
Guthaben=8000
Aktien=0
TradePrice=6.95
i=0
Periode=400
Graph=[]
redPeriode=int(Periode/numpy.e)
Werte=get_stocks_time_series(['NTDOY'])[0]
while i<(len(Werte)-Periode):
    BuyPreis,BuyPunkt=NEGmoddedOST(Werte[i:i+Periode])
    i+=BuyPunkt
    Buy(Werte[i],TradePrice,i)
    Graph.append(Guthaben+Aktien*Werte[i])
    if i>(len(Werte)-Periode):
        continue
    SellPreis,SellPunkt=moddedOST(Werte[i:i+Periode])
    i+=SellPunkt
    Sell(Werte[i],TradePrice,i)
    
    Graph.append(Guthaben+Aktien*Werte[i])
    
plt.subplot(2,2,1)
plt.title("Buy/Sell Decisions")
plt.scatter(XS,YS,s=100,c="g")
plt.scatter(XB,YB,s=100,c="r")

plt.plot([i for i in range(len(Werte))],Werte,"b-")
Guthaben+=Aktien*Werte[-1]
Aktien=0    
calc = numpy.round((Guthaben/8000.0), 3)
print(f"Factor {calc} after 20 years of Trading")

    
plt.subplot(2,2,2)
plt.title("Equity over Time")
plt.plot(Graph)
plt.plot([8000 for i in Graph])

plt.subplot(2,2,3)
plt.title("Fourier Noise Reduction")
plt.plot(numpy.fft.ifft([0 if abs(x)<3000 else x for x in numpy.fft.rfft(Werte)]))

plt.subplot(2,2,4)
plt.hist([S-B for B,S in zip(YB,YS)])
plt.title("Decision Effectiveness")



class Traders():
    def __init__(self):
        self.traders = []
        
    def traders(self, trader: Trader) -> Dict[str, int]:
        return self.traders.append(trader)

class Trader(Traders):
    def __init__(self):
        self.equity = None
        self.traders(self)
        
    def buy(self):
        self.equity = "new value"
        pass
    
    def sell(self):
        self.equity = "new value"
        pass
    
    @property
    def check_my_equity(self):
        return self.equity
    
    def go_trade(self):
        """ Implement the logic for trading.. your while loop ;) """
        pass


def main():
    ravid = Trader(name=Ravid, company=Babbel)
    dzenan = Trader(name=Dzenan)
    
    ravid.go_trade()
    
    
this_is_my_list = []
this_is_my_list = list()