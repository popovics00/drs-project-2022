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

    transactionsTemp = Cryptotransaction.query.all()
    transakcije = [] #transakcije korisnika
    for t in transactionsTemp:
        if t.senderId == id or t.senderId == id:
             transakcije.append(t.to_json())
    
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

    if(filterStatus == "SUCCESS"): 
        filterStatus = 2
    elif(filterStatus == "REJECTED"): 
        filterStatus = 1
    elif(filterStatus == "PROCESSING"): 
        filterStatus = 0

    if(filterCrypto != "0"):
        transakcije[:] = [transaction for transaction in transakcije if transaction['cryptocurrency'] == filterCrypto]
    if(filterPriceFrom != "0"):
        transakcije[:] = [transaction for transaction in transakcije if transaction['price'] >= float(filterPriceFrom)]
    if(filterPriceTo != "0"):
        transakcije[:] = [transaction for transaction in transakcije if transaction['price'] <= float(filterPriceTo)]
    if(filterTotalFrom != "0"):
        transakcije[:] = [transaction for transaction in transakcije if transaction['total'] >= float(filterTotalFrom)]
    if(filterTotalTo != "0"):
        transakcije[:] = [transaction for transaction in transakcije if transaction['total'] <= float(filterTotalTo)]
    if(filterAmountFrom != "0"):
        transakcije[:] = [transaction for transaction in transakcije if transaction['amount'] >= float(filterAmountFrom)]
    if(filterAmountTo != "0"):
        transakcije[:] = [transaction for transaction in transakcije if transaction['amount'] <= float(filterAmountTo)]
    if(filterDateFrom != "0"):
        transakcije[:] = [transaction for transaction in transakcije if transaction['date'] >= datetime.datetime.strptime(filterDateFrom, '%Y-%m-%d')]
    if(filterDateTo != "0"):
        transakcije[:] = [transaction for transaction in transakcije if transaction['date'] <= datetime.datetime.strptime(filterDateTo, '%Y-%m-%d')]
    if(filterSender != "0"):
        transakcije[:] = [transaction for transaction in transakcije if transaction['senderId'] == filterSender]
    if(filterReceiver != "0"):
        transakcije[:] = [transaction for transaction in transakcije if transaction['receiverId'] == filterReceiver]
    if(filterStatus != "0"):
        transakcije[:] = [transaction for transaction in transakcije if transaction['status'] == filterStatus]

    if len(transakcije) != 0:
        return jsonify(transakcije)
    else:
        return jsonify("Nemamo transakcija koje mozemo filtrirati!")


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