import pandas as pd
import os

class APIkeys():
    def __init__(self):
        self.fileName = 'exchangeCSV.csv'
        self.exchangesInfo = pd.DataFrame(
                index = ['upbit', 'kucoin', 'kraken', 'coss', 'bittrex', 'bitfinex', 'binance'],
                columns = ['exchange', 'id', 'apikey', 'secret']
                )
        
        self.exchangesInfo.at[:, 'exchange'] = ['upbit', 'kucoin', 'kraken', 'coss', 'bittrex', 'bitfinex', 'binance']
        if self.firstTime():
            self.write()
        self.exchangesInfo = self.read()


    def firstTime(self) -> bool: #vérifie si c'est la première connection
        if os.path.isfile(self.fileName):
            return False
        else:
            return True

    def read(self): #lecture du fichier
        with open(self.fileName, 'r') as f:
            exchangeCSV = pd.read_csv(f)    #voir si je fais un chiffrement
            return exchangeCSV

    def write(self): #écriture dans le fichier
        self.exchangesInfo.to_csv(self.fileName)
        
    def get(self):
        liste = []
        for i in self.exchangesInfo.index.values:
            if (type(self.exchangesInfo.at[i,'apikey']) == str and type(self.exchangesInfo.at[i,'secret']) == str):
                liste.append(self.exchangesInfo.iloc[i,:].tolist())
        return liste

    #management des clés API

    def editKeys(self, exchange: str, Id: str, apikey: str, secret: str):
        self.exchangesInfo.at[exchange,'id'] = Id
        self.exchangesInfo.at[exchange,'apikey'] = apikey
        self.exchangesInfo.at[exchange,'secret'] = secret
        self.write()
