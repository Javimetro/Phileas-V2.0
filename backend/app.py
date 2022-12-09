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

    # currentGame = Game(id)
    #
    # list = currentGame.getAiportsList(km_lkm)

    # return list

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

# http://127.0.0.1:5000/flyto?id=1&dest=LFPG&price=1000
@app.route('/flyto')
def flyto():
    args = request.args
    userid = args.get('id')
    destination = args.get('dest')
    price = int(args.get('price'))

    currentGame = Game(userid)
    balance = currentGame.tarkista_budjetti()
    if price > balance:
        return 'gameover'
    else:
        currentGame.fly(destination, price)
        status = currentGame.currentStatus()
        return json.dumps(status)


# http://127.0.0.1:5000/newgame?name=Lena
@app.route('/newgame')
def newgame():
    args = request.args
    user = args.get('name')

    game = Game(0, user)
    status = game.currentStatus()

    return json.dumps(status)


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=os.environ.get('PORT'))
