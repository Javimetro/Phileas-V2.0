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
    userId = args.get('id')
    km_lkm = args.get('km')
    YHTEINEN.valikoima(km_lkm,userId)
    vastaus = {
        'name':userId,
        'km_lkm':km_lkm,
        'vaihtoehdot':YHTEINEN.vaihtoehdot(km_lkm, userId)
    }
    jsonvast = json.dumps(vastaus)
    return Response(response=jsonvast, mimetype="application/json")

# http://127.0.0.1:5000/flyto?id=1&dest=LFPG
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
        'id': player,
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

    vastaus = YHTEINEN.getInfoById(userId)
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
