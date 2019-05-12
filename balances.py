import ccxt
import pandas as pd
import requests
import APIkeys_fetching
import fetchAddresses


def getAllSymbols():  # tous les symboles de d'adresse de cryptomonnaies supportés par l'API hybrix
    symbolsList = requests.get('https://api.hybrix.io/asset/').json()['data']
    return symbolsList


def fetchAddress(symbol: str, address: str):  # fetchAddress('btc', '385cR5DM96n1HvBDMzLHPYcw89fZAXULJP')
    """le symbol est à choisir parmis ceux de la liste retournés par getAllSymbols()"""
    request = requests.get(
        'https://api.hybrix.io/asset/' + symbol + '/balance/' + address).json()  # demande le montant de crypto sur cette adresse
    if request['error'] == 0:
        balance = requests.get(
            'https://api.hybrix.io/proc/' + str(request['data'])).json()  # api en deux étapes: deuxième montant
        if balance['data'] == None:
            balance['data'] = 0
        return balance['data']
    else:
        print('There is a probleme')


def getPrice(symbol: str, conversion: str) -> float:  # symbol: 'BTC', conversion: 'EUR'
    request = requests.get(
        'https://api.cryptonator.com/api/full/' + symbol + '-' + conversion).json()
    weightedPrice = request['ticker']['price']
    print(request)
    return float(weightedPrice)


def fetchExchangeBalance(exchange: str, apikey: str, secret: str):
    exchange_class = getattr(ccxt, exchange)
    exchange = exchange_class({'apikey':apikey , 'secret': secret, 'enableRateLimit': True})
    total = float()
    balances = exchange.fetchBalance()
    balances = pd.DataFrame(data=balances['info']['balances'])
    markets = exchange.loadMarkets()
    for i in balances.index:
        ticker = balances.loc[i, 'asset'] + '/BTC'
        if exchange.markets[ticker]:
            if float(balances.loc[i, 'free']) + float(
                    balances.loc[i, 'locked']) != 0:
                if balances.loc[i, 'asset'] == 'BTC':
                    balInBTC = float(balances.loc[i, 'free']) + float(
                        balances.loc[i, 'locked'])
                else:
                    if markets[ticker] != 0:
                        balInBTC = ticker['last'] * (
                            float(balances.loc[i, 'free']) + float(balances.loc[i, 'locked']))

        total += balInBTC

    return total

def compileBalances(self):#additione toutes les balances
    addresses = fetchAddresses.adresses()
    addresses = addresses.fetchAddresses.addressesList()
    totalBTC = float()
    for address in addresses:
        try:
            totalBTC += float(fetchAddress(symbol, address)) * \
                float(getPrice(symbol, 'BTC'))
        except:
            pass
    api = APIkeys()
    exchanges = api.get()
    for i,exchange in exchanges.iterrows():
        if (exchange['apikey'] != '' and exchange['secret'] != ''):
            try:
                totalBTC += float(fetchExchangeBalance(exchange)) * \
                    float(getPrice(symbol, 'BTC'))
            except:
                pass
    return totalBTC
