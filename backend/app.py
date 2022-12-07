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

# def fly(id, dest, consumption=0, player=None):
#     if id==0:
#         game = Game(0, dest, consumption, player)
#     else:
#         game = Game(id, dest, consumption)
#     game.location[0].fetchWeather(game)
#     nearby = game.location[0].find_nearby_airports()
#     for a in nearby:
#         game.location.append(a)
#     json_data = json.dumps(game, default=lambda o: o.__dict__, indent=4)
#     return json_data

@app.route('/kilometria/<km_lkm>')
def airportList(km_lkm):
    km_lkm = int(km_lkm)
    YHTEINEN.valikoima(km_lkm)
    vastaus = {
        'km_lkm':km_lkm,
        'vaihtoehdot':YHTEINEN.vaihtoehdot(km_lkm)
    }
    jsonvast = json.dumps(vastaus)
    return Response(response=jsonvast, mimetype="application/json")




# http://127.0.0.1:5000/flyto?game=fEC7n0loeL95awIxgY7M&dest=EFHK&consumption=123
@app.route('/km/<km_lkm>')
def flyto(km_lkm):
    km_lkm = float(km_lkm)


    vastaus = {
        'km_lkm': YHTEINEN.vaihtoehdot(km_lkm)
    }
    jsonvast = json.dumps(vastaus)
    return Response(response=jsonvast, mimetype="application/json")

    # args = request.args
    # id = args.get("game")
    # dest = args.get("dest")
    # consumption = args.get("consumption")
    # json_data = fly(id, dest, consumption)
    # print("*** Called flyto endpoint ***")
    # return json_data


# http://127.0.0.1:5000/newgame?player=Vesa&loc=EFHK
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
    YHTEINEN.updatelocation('EGLC')
    YHTEINEN.aloitusbudjetti()
    lat1 = YHTEINEN.haelatitude()
    lon1 = YHTEINEN.haelongitude()

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
    return jsonVast


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=os.environ.get('PORT'))
