import ccxt
import APIkeys_fetching
import errorMessage, validationMessage
from PyQt5 import QtCore, QtGui, QtWidgets


#Ordres ouverts
def openOrders(exchange: str):
    apikey = APIkeys_fetching()
    df = apikey.get()
    for i, row in df.iterrows():
        if df.loc[i]['exchange'] == exchange:
            apikey = df.loc[i,'apikey']
            secret = df.loc[i,'secret']
    exchange_class = getattr(ccxt,exchange)
    exchange = exchange_class({'apikey':apikey , 'secret': secret, 'enableRateLimit': True})
    if exchange.has['fetchOpenOrders']:
        exchange.options["warnOnFetchOpenOrdersWithoutSymbol"] = False
        openOders = []
        orders = exchange.fetchOpenOrders()
        for openOrder in orders:
            openOders.append([openOrder['id'], openOrder['symbol'], openOrder['side'], openOrder['price'], openOrder['amount']])
        return openOders#liste de liste [id, symbol, SELL/BUY, price, amount]

#Cancel order:
def cancelOrder(exchange: str, orderId, symbol: str): #ex: cancelOrder(binance, 11480381, 'MFT/BTC')
    apikey = APIkeys_fetching()
    df = apikey.get()
    for i, row in df.iterrows():
        if df.loc[i]['exchange'] == exchange:
            apikey = df.loc[i,'apikey']
            secret = df.loc[i,'secret']
    exchange_class = getattr(ccxt,exchange)
    exchange = exchange_class({'apikey':apikey , 'secret': secret, 'enableRateLimit': True})
    try:
        exchange.cancelOrder(orderId, symbol)
        return str('Order canceled')
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Responsemessage = QtWidgets.QDialog()
        ui = validationMessage.Ui_Responsemessage()
        validationMessage.ui.setupUi(Responsemessage)
        Responsemessage.show()
        sys.exit(app.exec_())
    except: #if there is an error
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Responsemessage = QtWidgets.QDialog()
        ui = errorMessage.Ui_Responsemessage()
        errorMessage.ui.setupUi(Responsemessage)
        Responsemessage.show()
        sys.exit(app.exec_())

      #(ex: cancelOrder(binance, 11480381, 'MFT/BTC'))
  
#créer un ordre
def createOrder(exchange: str, symbol: str, amount: float, price: float, side: str, type: str):# (side= 'buy' or 'sell'), type = 'limit' or 'market'
    #binance.create_order('RVN/BTC', 'limit', 'buy', amount = 1.0, price = 0.060154)
    apikey = APIkeys_fetching()
    df = apikey.get()
    for i, row in df.iterrows():
        if df.loc[i]['exchange'] == exchange:
            apikey = df.loc[i,'apikey']
            secret = df.loc[i,'secret']
    exchange_class = getattr(ccxt,exchange)
    exchange = exchange_class({'apikey':apikey , 'secret': secret, 'enableRateLimit': True})
    try:
        order = exchange.create_order(symbol, type, side, amount, price)
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Responsemessage = QtWidgets.QDialog()
        ui = validationMessage.Ui_Responsemessage()
        validationMessage.ui.setupUi(Responsemessage)
        Responsemessage.show()
        sys.exit(app.exec_())
    except:
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Responsemessage = QtWidgets.QDialog()
        ui = errorMessage.Ui_Responsemessage()
        errorMessage.ui.setupUi(Responsemessage)
        Responsemessage.show()
        sys.exit(app.exec_())
    return order
