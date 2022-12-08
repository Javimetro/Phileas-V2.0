import json
import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, Response, request
from flask_cors import CORS

import config
from game import Game
import YHTEINEN



load_dotenv()

app = Flask(__name__)
# lisätty cors
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Tietokantayhteys
config.conn = mysql.connector.connect(
         host=os.environ.get('HOST'),
         port= 3306,
         database=os.environ.get('DB_NAME'),
         user=os.environ.get('DB_USER'),
         password=os.environ.get('DB_PASS'),
         autocommit=True
         )


#http://127.0.0.1:5000/kilometria?id=1&km=1000
@app.route('/kilometria')
def airportList():
    args = request.args
    player = args.get('id')
    km_lkm = args.get('km')
    location = YHTEINEN.getInfoById(player)[3]
    YHTEINEN.valikoima(km_lkm,player)
    vaihtoehdotList = YHTEINEN.vaihtoehdot(km_lkm,player)

    for vaihtoehto in vaihtoehdotList:
        icao2 = vaihtoehto['ident']
        hinta = YHTEINEN.hintakaava(location,icao2)
        etaisyys = YHTEINEN.etaisyys(location,icao2)
        vaihtoehto['price']=round(hinta,1)
        vaihtoehto['distance']=int(etaisyys)

    vastaus = {
        'name': player,
        'km_lkm': km_lkm,
        'vaihtoehdot': vaihtoehdotList
    }
    jsonvast = json.dumps(vastaus)
    return Response(response=jsonvast, mimetype="application/json")


@app.route('/flyto')
def flyto():
    args = request.args
    player = args.get('id')
    destination = args.get('dest')

    location = YHTEINEN.getInfoById(player)[3]
    price = YHTEINEN.hintakaava(location, destination)
    money = YHTEINEN.lisaraha(price)

    YHTEINEN.updatelocation(destination, player)
    YHTEINEN.paivita_budjetti(price, money, player)

    info = YHTEINEN.getInfoById(player)
    jdata = {
        'player': player,
        'name': info[4],
        'location': destination,
        'budget': info[2],
        'consumed': info[1]
    }
    return json.dumps(jdata)

# http://127.0.0.1:5000/newgame?name=Lena
@app.route('/newgame')
def newgame():
    args = request.args
    user = args.get('name')
    sql = f'''INSERT INTO game SET screen_name = "{user}"'''
    kursori = config.conn.cursor()
    kursori.execute(sql)
    userId = kursori.lastrowid

    YHTEINEN.vuorot = 0
    YHTEINEN.lopullinenbudjetti = 0
    YHTEINEN.updatelocation('EGLC', userId)
    YHTEINEN.aloitusbudjetti(userId)

    sql = f'''SELECT * from game where id = "{userId}"'''
    kursori.execute(sql)
    vastaus = kursori.fetchone()

    jsonVast = {
        'id': vastaus[0],
        'name': vastaus[4],
        'location': vastaus[3],
        'budget': vastaus[2],
        'consumed': vastaus[1]
    }
    kursori.close()
    return json.dumps(jsonVast)


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=os.environ.get('PORT'))
