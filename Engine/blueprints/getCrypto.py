from flask import Blueprint, request, jsonify
from requests import Session
from models.user import User

from models.cryptocurrency import Cryptocurrency
from models.usercrypto import Usercrypto, UsercryptoSchema

getCrypto_bp = Blueprint('crypto', __name__)


#LISTA VALUTA KORISNIKA ZA DROPDOWN
@getCrypto_bp.route('/getUserCryptos', methods=['GET'])
def getUserCryptos():
    id = request.args.get("id")
    allUsersCryptos = Usercrypto.query.all()
    schema = UsercryptoSchema(many=True)
    myCripto = schema.dump(
        filter(lambda t: t.userId == id, allUsersCryptos)
    )
    cryptoNames = [o['cryptocurrency'] for o in myCripto]
    return jsonify(cryptoNames)



#FUNKCIJA VRACA LISTU VALUTA KOJE KORISNIK POSEDUJE
@getCrypto_bp.route('/accountCrypto', methods=['GET'])
def accountCrypto():
    id = request.args.get("id")

    allUsersCryptos = Usercrypto.query.all()
    schema = UsercryptoSchema(many=True)
    myCripto = schema.dump(
        filter(lambda t: t.userId == id, allUsersCryptos)
    )
    return jsonify(myCripto)



#LISTA SVIH KRIPTOVALUTA
@getCrypto_bp.route('/cryptolist', methods=['GET'])
def cryptolist():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'e29334cb-7952-4d4e-8b0a-19384c6b0dba'
    }

    parameters = {
        'start': '1',
        'limit': '50',
        'convert': 'USD'
    }

    session = Session()
    session.headers.update(headers)
    #saljemo zahtev na dati api sa parametrima koje trazi i dobijamo odgovor u json fajlu
    odgovorApia = session.get(url, params=parameters).json()
    odgovorValute = odgovorApia['data']
    valute = []

    #prolazimo kroz listu valuta
    for x in odgovorValute:
        name = x['name']
        price = x['quote']['USD']['price']
        change24h = x['quote']['USD']['percent_change_24h']
        pravimoValutu = Cryptocurrency(name, price, change24h)
        valute.append(pravimoValutu.to_json()) #pravimo valutu i pakujemo u json fajl

    return jsonify(valute)  #saljemo odgovor kao json