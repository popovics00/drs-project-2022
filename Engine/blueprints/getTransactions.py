from audioop import reverse
from flask import request, jsonify, Blueprint
import datetime

from models.cryptotransaction import Cryptotransaction

getTrans_bp = Blueprint('getTrans', __name__)
    
@getTrans_bp.route('/getMyTransactions', methods=['GET'])
def getMyTransactions():    
    id = request.args.get("id")

    transactionsList = []
    transactions = Cryptotransaction.query.all()
    for t in transactions:
        if t.receiverId == id or t.senderId == id:
            transactionsList.append(t.to_json())
            
    transactionsList.sort(key=lambda x: x['date'], reverse=True)

    if len(transactions) == 0:
        return jsonify("You have no transactions!")
    else:
        return jsonify(transactionsList)

@getTrans_bp.route('/filterTransactions', methods=['POST'])
def filterTransactions():
    id = request.form["id"]

    transactionsTemp = Cryptotransaction.query.all()
    transactions = []
    for t in transactionsTemp:
        if t.senderId == id or t.senderId == id:
             transactions.append(t.to_json())

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
        transactions[:] = [transaction for transaction in transactions if transaction['cryptocurrency'] == filterCrypto]
    
    if(filterAmountFrom != "0"):
        transactions[:] = [transaction for transaction in transactions if transaction['amount'] >= float(filterAmountFrom)]
    
    if(filterAmountTo != "0"):
        transactions[:] = [transaction for transaction in transactions if transaction['amount'] <= float(filterAmountTo)]
    
    if(filterPriceFrom != "0"):
        transactions[:] = [transaction for transaction in transactions if transaction['price'] >= float(filterPriceFrom)]
    
    if(filterPriceTo != "0"):
        transactions[:] = [transaction for transaction in transactions if transaction['price'] <= float(filterPriceTo)]
    
    if(filterTotalFrom != "0"):
        transactions[:] = [transaction for transaction in transactions if transaction['total'] >= float(filterTotalFrom)]
    
    if(filterTotalTo != "0"):
        transactions[:] = [transaction for transaction in transactions if transaction['total'] <= float(filterTotalTo)]
    
    if(filterSender != "0"):
        transactions[:] = [transaction for transaction in transactions if transaction['senderId'] == filterSender]
    
    if(filterReceiver != "0"):
        transactions[:] = [transaction for transaction in transactions if transaction['receiverId'] == filterReceiver]
    
    if(filterDateFrom != "0"):
        transactions[:] = [transaction for transaction in transactions if transaction['date'] >= datetime.datetime.strptime(filterDateFrom, '%Y-%m-%d')]
    
    if(filterDateTo != "0"):
        transactions[:] = [transaction for transaction in transactions if transaction['date'] <= datetime.datetime.strptime(filterDateTo, '%Y-%m-%d')]
    
    if(filterStatus == "SUCCESS"): 
        filterStatus = 2
    elif(filterStatus == "REJECTED"): 
        filterStatus = 1
    elif(filterStatus == "PROCESSING"): 
        filterStatus = 0

    if(filterStatus != "0"):
        transactions[:] = [transaction for transaction in transactions if transaction['status'] == filterStatus]

    if len(transactions) == 0:
        return jsonify("You have no transactions that correspond to that filter!")
    else:
        return jsonify(transactions)

@getTrans_bp.route('/getSortMyTransactions', methods=['POST'])
def getSortMyTransactions():
    id = request.form["id"]

    transactionsList = []
    transactions = Cryptotransaction.query.all()
    for t in transactions:
        if t.receiverId == id or t.senderId == id:
            transactionsList.append(t.to_json())

    sortBy = request.form['sortBy']
    sortAscDesc = request.form['sortAscDesc']

    if(sortBy == "Price"):
        if(sortAscDesc == "Ascending"):
            transactionsList.sort(key=lambda x: x['price'])
        else:
            transactionsList.sort(key=lambda x: x['price'], reverse=True)
    elif(sortBy == "Amount"):
        if(sortAscDesc == "Ascending"):
            transactionsList.sort(key=lambda x: x['amount'])
        else:
            transactionsList.sort(key=lambda x: x['amount'], reverse=True)
    elif(sortBy == "Date"):
        if(sortAscDesc == "Ascending"):
            transactionsList.sort(key=lambda x: x['date'])
        else:
            transactionsList.sort(key=lambda x: x['date'], reverse=True)
    elif(sortBy == "Total"):
        if(sortAscDesc == "Ascending"):
            transactionsList.sort(key=lambda x: x['total'])
        else:
            transactionsList.sort(key=lambda x: x['total'], reverse=True)

    return jsonify(transactionsList)