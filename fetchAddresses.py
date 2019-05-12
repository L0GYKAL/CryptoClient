import os
import pandas as pd
class addresses():
    def __init__(self):
        self.addressesInfo = pd.DataFrame(columns=['id', 'address', 'symbol'])
        if os.path.isfile('addresseInfo.csv'):
            with open('addresseInfo.csv', 'r') as f:
                self.addressesInfo = pd.read_csv(f)
        else:
            f = open('addresseInfo.csv', 'a')
            f.close()
            self.addressesInfo = pd.DataFrame(
                columns=['id', 'address', 'symbol'])
            self.addressesInfo.to_csv('addresseInfo.csv')

    def add(self, Id, address, symbol):
        i = len(self.addressesInfo.index)
        self.addressesInfo.at[i,'id']= Id
        self.addressesInfo.at[i,'address']= address
        self.addressesInfo.at[i,'symbol'] = symbol
        self.addressesInfo.to_csv('addresseInfo.csv')
        
    def addressesList(self):
        print(self.addressesInfo)
        liste = []
        for i in self.addressesInfo.index.values:
            liste.append(self.addressesInfo.iloc[i,:].tolist())
        return liste
    

