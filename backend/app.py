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


@app.route('/flyto')
def flyto():
    args = request.args
    player = args.get('id')
    destination = args.get('dest')
    YHTEINEN.updatelocation(destination, player)
    location = YHTEINEN.phileaslocation(player)
    jdata = {
        'player': player,
        'location': destination,
        'lat': location[0],
        'lon': location[1]
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
