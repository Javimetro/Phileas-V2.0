import json
import string, random
import config

import YHTEINEN
from airport import Airport
from goal import Goal
import config

class Game:

    # def __init__(self, id, loc, consumption, player=None):
    #     self.status = {}
    #     self.location = []
    #     self.goals = []

    def __init__(self, id, name=None):
        self.status = {}
        self.id = id

        if id == 0:
            # new game
            # Create new game id

            self.status = self.set_newgame(name)

            # self.location.append(Airport(loc, True))
            #self.player = player
            # Insert new game into DB
            # sql = "INSERT INTO Game VALUES ('" + self.status["id"] + "', " + str(self.status["co2"]["consumed"])
            # sql += ", " + str(self.status["co2"]["budget"]) + ", '" + loc + "', '" + self.status["name"] + "')"
            # print(sql)
            # cur = config.conn.cursor()
            # cur.execute(sql)
            #config.conn.commit()

        else:
            #update consumption and budget
            # sql2 = "UPDATE Game SET co2_consumed = co2_consumed + " + consumption + ", co2_budget = co2_budget - " + consumption + " WHERE id='" + id + "'"
            # print(sql2)
            # cur2 = config.conn.cursor()
            # cur2.execute(sql2)

            # find game from DB
            findgame = YHTEINEN.getInfoById(name)
            if len(findgame) == 1:
                # game found
                self.status = {
                    "id": findgame[0],
                    "name": findgame[4],
                    'location': findgame[3],
                    "consumed": findgame[1],
                    "budget": findgame[2]
                }
                # old location in DB currently not used
                # apt = Airport(loc, True)
                # self.location.append(apt)
                # self.set_location(apt)

            else:
                print("************** PELIÄ EI LÖYDY! ***************")

        # read game's goals
        # self.fetch_goal_info()


    def set_newgame(self, name):
        sql = f'''INSERT INTO game SET screen_name = {name}'''
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

    # def set_location(self, sijainti):
    #     #self.location = sijainti
    #     sql = "UPDATE Game SET location='" + sijainti.ident + "' WHERE id='" + self.status["id"] + "'"
    #     print(sql)
    #     cur = config.conn.cursor()
    #     cur.execute(sql)
        #config.conn.commit()
        #self.loc = sijainti.ident


    # def fetch_goal_info(self):
    #
    #     sql = "SELECT * FROM (SELECT Goal.id, Goal.name, Goal.description, Goal.icon, goal_reached.game_id, "
    #     sql += "Goal.target, Goal.target_minvalue, Goal.target_maxvalue, Goal.target_text "
    #     sql += "FROM Goal INNER JOIN goal_reached ON Goal.id = goal_reached.goal_id "
    #     sql += "WHERE goal_reached.game_id = '" + self.status["id"] + "' "
    #     sql += "UNION SELECT Goal.id, Goal.name, Goal.description, Goal.icon, NULL, "
    #     sql += "Goal.target, Goal.target_minvalue, Goal.target_maxvalue, Goal.target_text "
    #     sql += "FROM Goal WHERE Goal.id NOT IN ("
    #     sql += "SELECT Goal.id FROM Goal INNER JOIN goal_reached ON Goal.id = goal_reached.goal_id "
    #     sql += "WHERE goal_reached.game_id = '" + self.status["id"] + "')) AS t ORDER BY t.id;"
    #
    #     print(sql)
    #     cur = config.conn.cursor()
    #     cur.execute(sql)
    #     res = cur.fetchall()
    #     for a in res:
    #         if a[4]==self.status["id"]:
    #             is_reached = True
    #         else:
    #             is_reached = False
    #         goal = Goal(a[0], a[1], a[2], a[3], is_reached, a[5], a[6], a[7], a[8])
    #         self.goals.append(goal)
    #     return
