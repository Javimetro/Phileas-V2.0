import requests
#import config
#import os
from airport import Airport


#import json

from dotenv import load_dotenv
load_dotenv()


class Weather:


    def __init__(self, cur_icao):

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
    ##