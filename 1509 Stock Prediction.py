# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 11:57:48 2019

@author: User
"""
import requests
import json
import matplotlib.pyplot as plt
import numpy
"""this iteration looks like its performing fucking insanely good, but its not refactored yet, so pretty unreadable, and its also having some display errros (multiple sells after another)"""

def Trend(List):
    return List[-1]-List[0]

def Var(List):
    avg=sum(List)/len(List)
    return sum([numpy.square(x-avg) for x in List])/len(List)


def NEGmoddedOST(List):
    stop=int(len(List)/numpy.e)
    Estimate=min(List[:stop])
    avg=sum(List[:stop])/stop
    for i in range(stop,len(List)):
        Entry=List[i]
        Needed=avg+(Estimate-avg)*(1-(i-stop)/(len(List)-stop))
        if Entry<Needed:
            return Entry,i
    return Entry,i

def moddedOST(List):
    stop=int(len(List)/numpy.e)
    Estimate=max(List[:stop])
    avg=sum(List[:stop])/stop
    for i in range(stop,len(List)):
        Entry=List[i]
        Needed=avg+(Estimate-avg)*(1-(i-stop)/(len(List)-stop))
        if Entry>Needed:
            return Entry,i
    return Entry,i

Datum=[]
NeueDaten=requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=NTDOY&interval=1min&outputsize=full&apikey=SARLUC149FRWL21N")
new=json.loads(NeueDaten.content)
Keys=list(reversed(list(new["Time Series (Daily)"].keys())))
Werte=[float(new["Time Series (Daily)"][Key]["4. close"]) for Key in Keys]

print("Data ranging from {0} to {1} of DAX".format(Keys[0],Keys[-1]))

def Buy(Preis,Gebühren):
    global Guthaben
    global Aktien
    Guthaben-=Gebühren
    while Preis<Guthaben:
        Aktien+=1
        Guthaben-=Preis
        
def Sell(Preis,Gebühren):
    global Guthaben
    global Aktien
    Guthaben-=Gebühren
    while Aktien>0:
        Aktien-=1
        Guthaben+=Preis


XB=[]
YB=[]
XS=[]
YS=[]
Guthaben=8000
Aktien=0
TradePrice=6.95
i=0
Periode=200
Graph=[]
while i<(len(Werte)-Periode):
    if Trend(Werte[i:i+Periode])>2*Var(Werte[i:i+Periode]):
        Buy(Werte[i],TradePrice)
        XB.append(i)
        YB.append(Werte[i])
        print('Waiting to sell in Period:',i)
        while Trend(Werte[i:i+Periode])>2*numpy.sqrt(Var(Werte[i:i+Periode])):
            i+=1
        print(i)
    else:
        BuyPreis,BuyPunkt=NEGmoddedOST(Werte[i:i+Periode])
        i+=BuyPunkt
        Buy(BuyPreis,TradePrice)
        XB.append(i)
        YB.append(BuyPreis)
    if i>(len(Werte)-Periode):
        continue
    if Trend(Werte[i:i+Periode])<-2*numpy.sqrt(Var(Werte[i:i+Periode])):
        Sell(Werte[i],TradePrice)
        XS.append(i)
        YS.append(Werte[i])
        print('Waiting to Buy in Period',i)
        while Trend(Werte[i:i+Periode])<-2*numpy.sqrt(Var(Werte[i:i+Periode])):
            i+=1
        print(i)
    else:
        SellPreis,SellPunkt=moddedOST(Werte[i:i+Periode])
        i+=SellPunkt
        Sell(SellPreis,TradePrice)
        XS.append(i)
        YS.append(SellPreis)
    Graph.append(Guthaben)
    
plt.subplot(2,2,1)
plt.title("Buy/Sell Decisions")
plt.scatter(XB,YB,s=100,c="g")
plt.scatter(XS,YS,s=100,c="r")

plt.plot([i for i in range(len(Werte))],Werte,"b-")
Guthaben+=Aktien*Werte[-1]
Aktien=0    
print("{0}% increase nach 20 Jahren Trading".format(Guthaben/8000*100))
plt.subplot(2,2,2)
plt.title("Guthaben über Zeit")
plt.plot(Graph)
plt.plot([8000 for i in Graph])

plt.subplot(2,2,3)
plt.title("Fourier Noise Reduction")
plt.plot(numpy.fft.ifft([0 if abs(x)<1000 else x for x in numpy.fft.rfft(Werte)]))

plt.subplot(2,2,4)
plt.hist([S-B for B,S in zip(YB,YS)])
plt.title("Decission Effectiveness")
