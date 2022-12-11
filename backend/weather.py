import requests
import config
import os
from app import Airport
import mysql.connector
#import json

from dotenv import load_dotenv
load_dotenv()

config.conn = mysql.connector.connect(
         host=os.environ.get('HOST'),
         port= 3306,
         database=os.environ.get('DB_NAME'),
         user=os.environ.get('DB_USER'),
         password=os.environ.get('DB_PASS'),
         autocommit=True
         )
class Weather:


    def __init__(self, cur_icao):
        #air = Airport(userId)
        apikey = 'b506dbf5aa172758d111318ced349bb3'

        request = "https://api.openweathermap.org/data/2.5/weather?lat=" + \
                 str(Airport.haeLatLong(cur_icao)[0][0]) + "&lon=" + str(Airport.haeLatLong(cur_icao)[0][1]) + "&appid=" + apikey + "&units=metric"
        self.vastaus = requests.get(request).json()


    def weatherJson(self):

        self.json = {
            'main' : self.vastaus["weather"][0]["main"],
            'description' : self.vastaus["weather"][0]["description"],
            'temp' : self.vastaus["main"]["temp"],
            'humidity' : self.vastaus["main"]["humidity"],
        }
        print(self.json)
        return self.json

w = Weather(1) #test
w.weatherJson()