from multiprocessing.dummy import Process
from threading import Timer
from flask import request, jsonify, Blueprint
from requests import Session
from db_config import db
from datetime import timedelta
import random, datetime, sha3
from enum import Enum
from models.usercrypto import Usercrypto
from models.user import User
from models.cryptotransaction import Cryptotransaction


class StatusTransakcije(Enum):
    Processing = 0,
    Rejected = 1,
    Approved = 2

transactionCrypto_bp = Blueprint('transactionCrypto', __name__)

#FUNKCIJA KOJA RADI KUPOVINU KRIPTOVALUTA I PRAVI TRANSAKCIJU
@transactionCrypto_bp.route('/buycrypto', methods=['POST'])
def buycrypto():
    #kupimo parametre koje smo prosledili i dobavljamo kupca iz baze
    userId = request.form['id']
    amount = request.form['amount']
    crypto = request.form['crypto']
    price = request.form['price']

    kupac = User.query.get(userId)

    #PRAVIMO TRANSAKCIJU
    id = str(random.getrandbits(128))
    transaction = Cryptotransaction(receiverId = userId, 
                              senderId = '/', 
                              cryptocurrency = crypto, 
                              amount= amount, 
                              price = price, 
                              total = float(amount) * float(price), 
                              transactionId = id, date = datetime.datetime.now(), 
                              status = StatusTransakcije.Rejected.value[0])

    #PROVERA DA LI IMAMO DOVOLJNO NOVCA
    if(float(amount) * float(price) <= kupac.balance):
        cryptoWalets = Usercrypto.query.all()
        postojiWalletZaTuValutu = False
        #prolazimo kroz sve wallete i proveravamo da li korisnik vec ima tu valutu ako ima samo uvecamo iznos
        for wallet in cryptoWalets:
            if(wallet.userId == userId and wallet.cryptocurrency == crypto):
                wallet.balance += float(amount)
                db.session.add(wallet)
                db.session.commit()
                kupac.balance -= float(amount) * float(price) #smanjujemo iznos novca za cenu kupljene valute
                db.session.add(kupac)
                db.session.commit()
                postojiWalletZaTuValutu = True
        #ako nema tu valutu onda mu dodajemo valutu
        if(postojiWalletZaTuValutu == False):
            cryptoWallet = Usercrypto(userId = userId, cryptocurrency = crypto, balance = float(amount))
            try:
                db.session.add(cryptoWallet)
                db.session.commit()  
                kupac.balance -= float(amount) * float(price) #smanjujemo iznos novca za cenu kupljene valute
                db.session.add(kupac)
                db.session.commit()   
            except Exception as e:
                print(str(e))
                return jsonify(e), 400
        #status transakcije stavljamo na approved jer smo uspeli da dodamo wallet
        transaction.status = StatusTransakcije.Approved.value
        db.session.add(transaction)
        db.session.commit()
        return jsonify("Uspesno ste kupili kripto valutu!"), 200
    else:
        db.session.add(transaction)
        db.session.commit()
        return jsonify('Nemate dovoljno novca da bi obavili ovu transakciju!'), 200



#FUNKCIJA KOJA KONVERTUJE VALUTE
@transactionCrypto_bp.route('/confirmConversion', methods=['POST'])
def confirmConversion():
    #pribavljamo parametre
    id = request.form["id"]
    myCrypto = request.form["myCrypto"]
    allCryptos = request.form["allCryptos"]
    inputConvertAmount = request.form["inputConvertAmount"]
    cryptoValue = request.form["cryptoValue"]
    myCryptoValue = request.form["myCryptoValue"]
    allWallets = Usercrypto.query.all() #svi walleti
    allWalletsMyUser = [] #svi walleti od datog korisnika
    postojiWallet = False
    
    idd = str(random.getrandbits(128))
    transaction = Cryptotransaction(receiverId = id, 
                              senderId = '/', 
                              cryptocurrency = allCryptos, 
                              amount = inputConvertAmount, 
                              price = cryptoValue, 
                              total = float(inputConvertAmount) * float(cryptoValue), 
                              transactionId = idd, 
                              date = datetime.datetime.now(), 
                              status = StatusTransakcije.Rejected.value[0])
    
    #prolazimo kroz listu svih walleta i odvajamo one koji odgovaraju nasem korisniku
    for c in allWallets:
        if(c.userId == id):
            allWalletsMyUser.append(c)
            if(c.cryptocurrency == myCrypto):
                valutaKojuMenjamo = c
            if(c.cryptocurrency == allCryptos):
                valutaUKojuMenjamo = c
                postojiWallet = True
                
    kolikoVrediMoje = float(inputConvertAmount) * float(myCryptoValue)
    kolicinaNoveValute = kolikoVrediMoje / float(cryptoValue)
    
    transaction.amount = kolicinaNoveValute
    transaction.price = cryptoValue
    transaction.total = kolikoVrediMoje

    if(valutaKojuMenjamo.balance < float(inputConvertAmount)): #nema dovoljno da bi promenio
        db.session.add(transaction)
        db.session.commit()
        return jsonify('Nemate dovoljno date valute.')
    
    #oduzimamo onoliko koliko smo promenili
    valutaKojuMenjamo.balance -= float(inputConvertAmount)
    if(valutaKojuMenjamo.balance == 0): #ako smo sve izmenili samo obrisemo wallet
        db.session.delete(valutaKojuMenjamo)
        db.session.commit()
    else: #samo update
        db.session.add(valutaKojuMenjamo)
        db.session.commit()
    
    if(postojiWallet):  #ako posoji samo povecamo vrednost
        valutaUKojuMenjamo.balance += kolicinaNoveValute
        db.session.add(valutaUKojuMenjamo)
        db.session.commit()
        
        transaction.status = StatusTransakcije.Approved.value
        db.session.add(transaction)
        db.session.commit()
    else: #ako ne postoji dodavmo novi
        newCrypto = Usercrypto(userId = id, cryptocurrency = allCryptos, balance = float(kolicinaNoveValute))
        try:
            db.session.add(newCrypto)
            db.session.commit()
            
            transaction.status = StatusTransakcije.Approved.value
            db.session.add(transaction)
            db.session.commit()
        except Exception as e:
            return jsonify(e), 400

    return jsonify("Uspesna transakcija.")

#FUNKCIJA THREAD KOJA TRANSAKCIJU APPROVA I VRSI PRENOS VALUTE AKO SU USLOVI OK
def obradaTransakcije():
    Timer(0.5, obradaTransakcije, []).start() #timer pocinje da broji 20sekundi jer je 5minuta dugo pa da ne cekamo dzabe
    transakcije = Cryptotransaction.query.all() #lista transakcija
    db.session.remove()
    wallets = Usercrypto.query.all() #lista walleta
    db.session.remove()
    users = User.query.all()  #lista korisnika
    db.session.remove()


    for t in transakcije: # prolazimo kroz listu transakcija kako bi nasli transakciju koja treba da se approva
        if t.status == 0 and t.date + timedelta(minutes = 0.5)  < datetime.datetime.today():        
            korisnikPostoji = False
            wallet = object

            for w in wallets:
                if w.userId == t.senderId and w.cryptocurrency == t.cryptocurrency:
                    wallet = w
            for user in users:
                if(user.id == int(t.receiverId)):
                    korisnikPostoji = True

            if t.senderId == t.receiverId: # OTKACI AKO SAM SEBI SALJE
                t.status = StatusTransakcije.Rejected.value[0]
                db.session.add(t)
                db.session.commit()
            elif korisnikPostoji == False: # OTKACI AKO KORISNIK KOME SALJEMO NE POSTOJI
                t.status = StatusTransakcije.Rejected.value[0]
                db.session.add(t)
                db.session.commit()
            elif wallet.balance  < t.amount: #AKO NEMA DOVOLJNO NOVCA
                t.status = StatusTransakcije.Rejected.value[0]
                db.session.add(t)
                db.session.commit()
            else: # PRIHVATI
                t.status = StatusTransakcije.Approved.value
                db.session.add(t)
                db.session.commit()

                walletPrimaocaNePostoji = True

                for wa in wallets:
                    if wa.userId == t.receiverId and wa.cryptocurrency == t.cryptocurrency: #dodali senderu
                        walletPrimaocaNePostoji = False
                        wa.balance += t.amount
                        db.session.add(wa)
                        db.session.commit()
                    if wa.userId == t.senderId and wa.cryptocurrency == t.cryptocurrency: #ovde smo samo oduzeli od sendera
                        wa.balance -= t.amount
                        if(wa.balance == 0): #ako posaljemo sve sto imamo iz neke valute, da se obrise iz baze
                            db.session.delete(wa)
                            db.session.commit()
                        db.session.add(wa)
                        db.session.commit()

                if walletPrimaocaNePostoji: #ako ne postojipravimo novi wallet
                    newUserCrypto = Usercrypto(userId = t.receiverId,
                                            cryptocurrency = t.cryptocurrency,
                                            balance = t.amount)
                    
                    db.session.add(newUserCrypto)
                    db.session.commit()
    
#POKRETANJE THREADA ZA APPROVE
@transactionCrypto_bp.before_app_first_request
def threadStart():
    obradaTransakcije()

#POZIVAMO JE KAO PROCES
def pravljenjeTransakcije(senderId, receiverId, crypto, url, amount):
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'e29334cb-7952-4d4e-8b0a-19384c6b0dba'
    }

    delici = crypto.split()
    cryptoTemp = '-'
    cryptoTemp = cryptoTemp.join(delici)
    parametri = {'slug': cryptoTemp.lower(), 'convert': 'USD'}

    #ponvo gadjamo api kako bi nasli kripto valutu da bi mogli koristiti njenu cenu
    session1 = Session()
    session1.headers.update(headers)
    response = session1.get(url, params=parametri).json()

    valuta = response['data']

    id = ''
    for key, value in valuta.items():
        id = key

    cenaValute = valuta[key]['quote']['USD']['price']
    id = str(senderId) + str(receiverId) + amount + str(random.randint(0, 1000)) 
    
    k = sha3.keccak_256()
    k.update(str(id).encode('utf-8'))
    id = k.hexdigest()

    #pravimo transakciju i upisujemo je
    transakcijaNova = Cryptotransaction(receiverId = str(receiverId),
                            senderId = str(senderId),
                            cryptocurrency = crypto,
                            amount= amount, 
                            price = cenaValute,
                            total = float(amount) * float(cenaValute),
                            transactionId = id,
                            date = datetime.datetime.now(),
                            status = StatusTransakcije.Processing.value[0])
    try:
        db.session.add(transakcijaNova)
        db.session.commit()
    except Exception as e:
        print('database error')
        print(str(e))



#FUNKCIJA KOJU GADJAMO KADA SALJEMO PARE SA NALOGA NA NALOG
@transactionCrypto_bp.route('/executeTransaction', methods=['POST'])
def executeTransaction():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    #pribavljanje parametara
    senderId = request.form["id"]
    receiverEmail = request.form['receiveremail']
    receiverId = -1
    users = User.query.all()
    for u in users:
        if u.email == receiverEmail:
            receiverId = u.id
    crypto = request.form['crypto']
    amount = request.form['value']

    processZaPravljenjeTransakcije = Process(target = pravljenjeTransakcije, args=(senderId, receiverId, crypto, url, amount, ))
    processZaPravljenjeTransakcije.daemon = True # rad procesa bez nadzora
    processZaPravljenjeTransakcije.start()

    return 'Transakcija je poslata na izvrsavanje. (za 5 minuta ce biti obradjena)', 200