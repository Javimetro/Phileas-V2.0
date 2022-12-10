import random
import os
import config
#from weather import Weather
#from geopy import distance
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



    def haeLatLong(self):
        sql = f'''select latitude_deg, longitude_deg from airport, game where game.id={self.userId} and location = ident'''
        kursori = config.conn.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        self.lat = float(tulos[0][0])
        #print(f'lat on: {self.lat}')
        self.long = float(tulos[0][1])
        #print(f'long on: {self.long}')
        return tulos

    def valikoima(self, kilometrit):
        self.kilometrit = kilometrit
        lat = self.haeLatLong()[0][0]
        long = self.haeLatLong()[0][1]
        northlimit = float(lat) + float(kilometrit) * float(0.01)
        southlimit = float(lat) - float(kilometrit) * float(0.01)
        westlimit = float(long)
        eastlimit = float(long) + float(kilometrit) * float(0.01)
        if -180 < eastlimit < 180:
            sql = f'''SELECT ident, name, latitude_deg, longitude_deg
                FROM Airport WHERE (type LIKE 'medium%' OR type LIKE'large%') AND latitude_deg BETWEEN {southlimit} AND {northlimit}
                AND longitude_deg BETWEEN {westlimit} AND {eastlimit}'''
        elif eastlimit > 180:
            eastlimit = eastlimit - 360

            sql = f'''SELECT ident, name, latitude_deg, longitude_deg
                FROM Airport WHERE (type LIKE 'medium%' OR type LIKE'large%') AND latitude_deg BETWEEN {southlimit} AND {northlimit}
                AND longitude_deg BETWEEN {-180} AND {eastlimit} AND {westlimit} AND {180}'''

        kursori = config.conn.cursor(dictionary=True)
        kursori.execute(sql)
        tulos = kursori.fetchall()
        print(tulos)
        return tulos




    def vaihtoehdot(self, kilometrit):
        self.kilometrit = kilometrit
        vaihtoehdot1 = []
        tulos = self.valikoima(self.userId,)
        for i in range(10):
            vaihtoehdot1.append(random.choice(tulos))
        #print(vaihtoehdot1)
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

    def city_country(self):
        sql = f'''select airport.municipality, country.name from airport, country, game 
        where game.id={self.userId} and  game.location=airport.ident and airport.iso_country=country.iso_country;'''
        kursori = config.conn.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        for i in tulos:
            print(f'{i[0]} ,{i[1]}')

