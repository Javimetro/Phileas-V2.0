
from geopy.distance import geodesic
import config

class Game:

    def __init__(self, userid, name=None):
        self.status = {}

        self.gameover = False

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

        # vuorot = 0
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
            'consumed': info[1]
        }
        kursori.close()
        return jdata

    def set_budget(self):
        sql = f'''UPDATE game SET co2_budget=1000, co2_consumed=0 WHERE id={self.id}'''
        kursori = config.conn.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchone()
        return tulos

    def update_budget(self, hinta, raha):
        sql = f'''UPDATE game SET co2_budget=co2_budget-{hinta}+{raha}, co2_consumed=co2_consumed+{hinta} WHERE id={self.id}'''
        kursori = config.conn.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchone()
        return tulos

    def fly(self, dest, price):
        self.updatelocation(dest)
        # location = self.currentStatus()["location"]
        # price = self.get_price(location, dest)
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
