
from geopy.distance import geodesic
import config
from airport import Airport


class Game:

    def __init__(self, userid, name=None):
        self.status = {}

        if userid == 0:
            # new game
            # Create new game id
            self.set_newgame(name)
        else:
            self.id = userid

    def set_newgame(self, name):
        sql = f'''INSERT INTO game SET screen_name = "{name}"'''
        kursori = config.conn.cursor()
        kursori.execute(sql)
        self.id = kursori.lastrowid

        self.updatelocation('EGLC')
        self.set_budget()
        kursori.close()
        return

    def updatelocation(self, icao):
        sql = f'''UPDATE game SET location= %s WHERE id={self.id}'''
        tuple = (icao,)
        kursori = config.conn.cursor()
        kursori.execute(sql, tuple)

    def currentStatus(self):
        sql = f'''select * from game where game.id={self.id}'''
        kursori = config.conn.cursor()
        kursori.execute(sql)
        info = kursori.fetchone()
        jdata = {
            'id': self.id,
            'name': info[4],
            'location': info[3],
            'budget': info[2],
            'consumed': info[1],
            'distance': info[5],
            'times': info[6]
        }
        kursori.close()
        return jdata

    def set_budget(self):
        sql = f'''UPDATE game SET co2_budget=1300, co2_consumed=0, kilometrit_yht=0, vuorot_yht=0 WHERE id={self.id}'''
        kursori = config.conn.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchone()
        return tulos

    def update_budget(self, hinta, raha):
        sql = f'''UPDATE game SET co2_budget=co2_budget-{hinta}+{raha}, co2_consumed=co2_consumed+{hinta}, 
        vuorot_yht=vuorot_yht+1 WHERE id={self.id}'''
        kursori = config.conn.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchone()
        return tulos

    def fly(self, dest, price):
        self.updatelocation(dest)

        raha = self.lisaraha(price)
        self.update_budget(price, raha)


    def lisaraha(self, hinta):
        raha = hinta * 0.5
        return raha


    def tarkista_budjetti(self):
        sql = f'''SELECT co2_budget FROM game WHERE id={self.id}'''
        kursori=config.conn.cursor()
        kursori.execute(sql)
        tulos=kursori.fetchone()
        return tulos[0]

    def update_kilometrit(self, distance):
        sql = f'''UPDATE game SET kilometrit_yht=kilometrit_yht+{distance} WHERE id={self.id}'''
        kursori = config.conn.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchone()
        return tulos

