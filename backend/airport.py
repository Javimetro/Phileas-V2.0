import random
import os
import config
from weather import Weather
from geopy import distance
import mysql.connector



config.conn = mysql.connector.connect(
         host=os.environ.get('HOST'),
         port= 3306,
         database=os.environ.get('DB_NAME'),
         user=os.environ.get('DB_USER'),
         password=os.environ.get('DB_PASS'),
         autocommit=True
         )

class Airport:

    def __init__(self,userId):
        self.userId = userId



    def haeLatLong(self, userId):
        sql = f'''select latitude_deg, longitude_deg from airport, game where game.id={userId} and location = ident'''
        kursori = config.conn.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        self.lat = float(tulos[0][0])
        print(f'lat on: {self.lat}')
        self.long = float(tulos[0][1])
        print(f'long on: {self.long}')
        return tulos

    def valikoima(self, userId, kilometrit):
        self.kilometrit = kilometrit
        lat = air.haeLatLong(userId)[0][0]
        long = air.haeLatLong(userId)[0][1]
        northlimit = lat + kilometrit * 0.01
        southlimit = lat - kilometrit * 0.01
        westlimit = long
        eastlimit = long + kilometrit * 0.01
        if -180 < eastlimit < 180:
            sql = f'''SELECT ident, name, latitude_deg, longitude_deg
                FROM Airport WHERE type='large_airport' OR type='medium_airport' AND latitude_deg BETWEEN {southlimit} AND {northlimit}
                AND longitude_deg BETWEEN {westlimit} AND {eastlimit}'''
        elif eastlimit > 180:
            eastlimit = eastlimit - 360

            sql = f'''SELECT ident, name, latitude_deg, longitude_deg
                FROM Airport WHERE type='large_airport' OR type='medium_airport' AND latitude_deg BETWEEN {southlimit} AND {northlimit}
                AND longitude_deg BETWEEN {-180} AND {eastlimit} AND {westlimit} AND {180}'''

        kursori = config.conn.cursor(dictionary=True)
        kursori.execute(sql)
        tulos = kursori.fetchall()
        print(tulos)
        return tulos

    def vaihtoehdot(self,userId, kilometrit):
        self.kilometrit = kilometrit
        vaihtoehdot1 = []
        tulos = air.valikoima(userId,kilometrit)
        for i in range(10):
            vaihtoehdot1.append(random.choice(tulos))
        return vaihtoehdot1

    def londoncityairport(self):
        sql = '''select ident, name, latitude_deg, longitude_deg
            from airport
            where ident = "EGLC"'''
        kursori = config.conn.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchone()
        print(tulos)
        return tulos

    def city_country(self,userId):
        sql = f'''select airport.municipality, country.name from airport, country, game 
        where game.id={userId} and  game.location=airport.ident and airport.iso_country=country.iso_country;'''
        kursori = config.conn.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        for i in tulos:
            print(f'{i[0]} ,{i[1]}')


air = Airport(1)
air.londoncityairport()





    # lisätty data, jottei tartte jokaista lentokenttää hakea erikseen
    # def __init__(self, ident, active=False, data=None):
    #     self.ident = ident
    #     self.active = active
    #
    #     # vältetään kauhiaa määrää hakuja
    #     if data is None:
    #         # find airport from DB
    #         sql = "SELECT ident, name, latitude_deg, longitude_deg FROM Airport WHERE ident='" + ident + "'"
    #         print(sql)
    #         cur = config.conn.cursor()
    #         cur.execute(sql)
    #         res = cur.fetchall()
    #         if len(res) == 1:
    #             # game found
    #             self.ident = res[0][0]
    #             self.name = res[0][1]
    #             self.latitude = float(res[0][2])
    #             self.longitude = float(res[0][3])
    #     else:
    #         self.name = data['name']
    #         self.latitude = float(data['latitude'])
    #         self.longitude = float(data['longitude'])


    # def find_nearby_airports(self):
    #     # print("Testing geopy...")
    #     # self.distanceTo(1, 2)
    #     lista = []
    #     # haetaan kaikki tiedot kerralla
    #     sql = "SELECT ident, name, latitude_deg, longitude_deg FROM Airport WHERE latitude_deg BETWEEN "
    #     sql += str(self.latitude - config.max_lat_dist) + " AND " + str(self.latitude + config.max_lat_dist)
    #     sql += " AND longitude_deg BETWEEN "
    #     sql += str(self.longitude - config.max_lon_dist) + " AND " + str(self.longitude + config.max_lon_dist)
    #     print(sql)
    #     cur = config.conn.cursor()
    #     cur.execute(sql)
    #     res = cur.fetchall()
    #     for r in res:
    #         if r[0] != self.ident:
    #             # lisätty data, jottei jokaista kenttää tartte hakea
    #             # uudestaan konstruktorissa
    #             data = {'name': r[1], 'latitude': r[2], 'longitude': r[3]}
    #             print(data)
    #             nearby_apt = Airport(r[0], False, data)
    #             nearby_apt.distance = self.distanceTo(nearby_apt)
    #             if nearby_apt.distance <= config.max_distance:
    #                 lista.append(nearby_apt)
    #                 nearby_apt.co2_consumption = self.co2_consumption(nearby_apt.distance)
    #     return lista
    #
    # def fetchWeather(self, game):
    #     self.weather = Weather(self, game)
    #     return
    #
    # def distanceTo(self, target):
    #
    #     coords_1 = (self.latitude, self.longitude)
    #     coords_2 = (target.latitude, target.longitude)
    #     dist = distance.distance(coords_1, coords_2).km
    #     return int(dist)
    #
    # def co2_consumption(self, km):
    #     consumption = config.co2_per_flight + km * config.co2_per_km
    #     return consumption
