from audioop import reverse
from flask import request, jsonify, Blueprint
import datetime

from models.cryptotransaction import Cryptotransaction

getTransactions_bp = Blueprint('getTransactions', __name__)
    

#FUNKCIJA KOJA VRACA SVE TRANSAKCIJE ZA DATOG KORISNIKA
@getTransactions_bp.route('/getMyTransactions', methods=['GET'])
def getMyTransactions():    
    id = request.args.get("id")

    listaTransakcija = [] #lista transakcija koje su naseg korisnika
    transactions = Cryptotransaction.query.all()
    for t in transactions:
        if t.receiverId == id or t.senderId == id:
            listaTransakcija.append(t.to_json())

    #sortiramo transakcije po datumu od najnovije
    listaTransakcija.sort(key=lambda x: x['date'], reverse=True)

    #ako imamo transakciju onda je saljemo kao json fajl
    if len(transactions) == 0:
        return jsonify("Nemate ni jednu transakciju!")
    else:
        return jsonify(listaTransakcija)


#FILTRACIJA TRANSAKCIJA
@getTransactions_bp.route('/filterTransactions', methods=['POST'])
def filterTransactions():
    id = request.form["id"]

    listaTransakcija = [] #lista transakcija koje su naseg korisnika
    transactions = Cryptotransaction.query.all()
    for t in transactions:
        if t.receiverId == id or t.senderId == id:
            listaTransakcija.append(t.to_json())
 
    #pribavljanje parametara
    filterCrypto = request.form["filterCrypto"]
    filterAmountFrom = request.form["filterAmountFrom"]
    filterAmountTo = request.form["filterAmountTo"]
    filterPriceFrom = request.form["filterPriceFrom"]
    filterPriceTo = request.form["filterPriceTo"]
    filterTotalFrom = request.form["filterTotalFrom"]
    filterTotalTo = request.form["filterTotalTo"]
    filterSender = request.form["filterSender"]
    filterReceiver = request.form["filterReceiver"]
    filterDateFrom = request.form["filterDateFrom"]
    filterDateTo = request.form["filterDateTo"]
    filterStatus = request.form["filterStatus"]

    if(filterCrypto != "0"):
        listaTransakcija[:] = [transaction for transaction in listaTransakcija if transaction['cryptocurrency'] == filterCrypto]
    
    if(filterAmountFrom != "0"):
        listaTransakcija[:] = [transaction for transaction in listaTransakcija if transaction['amount'] >= float(filterAmountFrom)]
    
    if(filterAmountTo != "0"):
        listaTransakcija[:] = [transaction for transaction in listaTransakcija if transaction['amount'] <= float(filterAmountTo)]
    
    if(filterPriceFrom != "0"):
        listaTransakcija[:] = [transaction for transaction in listaTransakcija if transaction['price'] >= float(filterPriceFrom)]
    
    if(filterPriceTo != "0"):
        listaTransakcija[:] = [transaction for transaction in listaTransakcija if transaction['price'] <= float(filterPriceTo)]
    
    if(filterTotalFrom != "0"):
        listaTransakcija[:] = [transaction for transaction in listaTransakcija if transaction['total'] >= float(filterTotalFrom)]
    
    if(filterTotalTo != "0"):
        listaTransakcija[:] = [transaction for transaction in listaTransakcija if transaction['total'] <= float(filterTotalTo)]
    
    if(filterSender != "0"):
        listaTransakcija[:] = [transaction for transaction in listaTransakcija if transaction['senderId'] == filterSender]
    
    if(filterReceiver != "0"):
        listaTransakcija[:] = [transaction for transaction in listaTransakcija if transaction['receiverId'] == filterReceiver]
    
    if(filterDateFrom != "0"):
        listaTransakcija[:] = [transaction for transaction in listaTransakcija if transaction['date'] >= datetime.datetime.strptime(filterDateFrom, '%Y-%m-%d')]
    
    if(filterDateTo != "0"):
        listaTransakcija[:] = [transaction for transaction in listaTransakcija if transaction['date'] <= datetime.datetime.strptime(filterDateTo, '%Y-%m-%d')]
    
    if(filterStatus == "SUCCESS"): 
        filterStatus = 2
    elif(filterStatus == "REJECTED"): 
        filterStatus = 1
    elif(filterStatus == "PROCESSING"): 
        filterStatus = 0

    if(filterStatus != "0"):
        listaTransakcija[:] = [transaction for transaction in listaTransakcija if transaction['status'] == filterStatus]
        return jsonify(listaTransakcija)

    if len(listaTransakcija) == 0:
        return jsonify("You have no transactions that correspond to that filter!")
    else:
        return jsonify(listaTransakcija)


#SORITRANJE TRANSAKCIJA
@getTransactions_bp.route('/getSortMyTransactions', methods=['POST'])
def getSortMyTransactions():
    #izvlacimo parametre
    id = request.form["id"]
    sortBy = request.form['sortBy']
    sortAscDesc = request.form['sortAscDesc']
    
    #izvlacimo transakcije korisnika
    transactions = Cryptotransaction.query.all()
    listaTransakcijaKorisnika = []
    for t in transactions:
        if t.receiverId == id or t.senderId == id:
            listaTransakcijaKorisnika.append(t.to_json())


    if(sortBy == "Price"):
        if(sortAscDesc == "Ascending"):
            listaTransakcijaKorisnika.sort(key=lambda x: x['price'])
        else:
            listaTransakcijaKorisnika.sort(key=lambda x: x['price'], reverse=True)
    elif(sortBy == "Date"):
        if(sortAscDesc == "Ascending"):
            listaTransakcijaKorisnika.sort(key=lambda x: x['date'])
        else:
            listaTransakcijaKorisnika.sort(key=lambda x: x['date'], reverse=True)
    elif(sortBy == "Amount"):
        if(sortAscDesc == "Ascending"):
            listaTransakcijaKorisnika.sort(key=lambda x: x['amount'])
        else:
            listaTransakcijaKorisnika.sort(key=lambda x: x['amount'], reverse=True)
    elif(sortBy == "Total"):
        if(sortAscDesc == "Ascending"):
            listaTransakcijaKorisnika.sort(key=lambda x: x['total'])
        else:
            listaTransakcijaKorisnika.sort(key=lambda x: x['total'], reverse=True)

    return jsonify(listaTransakcijaKorisnika)