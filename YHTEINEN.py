import mysql.connector
from geopy.distance import geodesic
import random
yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='rootformaria',
         autocommit=True
         )

def haelongitude():
    sql = '''SELECT longitude_deg FROM airport 
    WHERE name = "London City Airport"'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos

def haelatitude():
    sql = '''SELECT latitude_deg FROM airport 
    WHERE name = "London City Airport"'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos

def updatelocation(icao):
    sql = '''UPDATE game SET location= %s WHERE screen_name = "Phileas Fogg"'''
    tuple = (icao,)
    print(sql, tuple)
    kursori = yhteys.cursor()
    kursori.execute(sql,tuple)
    if kursori.rowcount == 1:
        print("LOCATION UPDATED")

lat1 = haelatitude()
lon1 = haelongitude()

print(f'Hei Phileas! Nyt olet London City Airportilla ja koordinaattisi ovat: {lat1[0],lon1[0]}')
distance = int(input(f'Kuinka monta kilometria haluaisit lentää ekalla matkallasi? ')) # kilometreina
northlimit = lat1[0] + distance*0.01
southlimit = lat1[0] - distance*0.01
westlimit = lon1[0] + distance*0.01
eastlimit = lon1[0] - distance*0.01

def valikoima():
    sql = f'''SELECT ident, name, latitude_deg, longitude_deg
    FROM Airport WHERE latitude_deg BETWEEN {southlimit} AND {northlimit}
    AND longitude_deg BETWEEN {eastlimit} AND {westlimit}'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

def vaihtoehdot():
    vaihtoehdot = {}
    for i in range(4):
        vaihtoehdot[i+1] = random.choice(valikoima())
    return vaihtoehdot

print(f'Sillä etäisyydellä voit matkustaa seuraaville lentokentille: {vaihtoehdot()}')
mihin = input(f'Valitse yksi niistä ja matkustetaan sille lentokentälle. Kirjoita ICAO-koodi:  ')

def etaisyysicaolla(icao):
    tuple = (icao,)
    sql = '''SELECT latitude_deg, longitude_deg 
    FROM airport 
    WHERE ident = %s'''
    kursori = yhteys.cursor()
    kursori.execute(sql, tuple)
    tulos = kursori.fetchone()
    return tulos

def phileaslocation():
    sql = '''select latitude_deg, longitude_deg
    from airport, game
    where screen_name = "Phileas Fogg" and location = ident'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    print(tulos)
    return tulos

icao1 = phileaslocation()
icao2 = mihin

etäisyys = print(f' Etäisyys lentokenttien välillä on: {round(geodesic(icao1, etaisyysicaolla(icao2)).km,3)} Km.')
varmistus = input(f'Oletko varma, että haluat matkustaa {mihin} lentokentälle (K/E)?: ')
#while varmistus == 'K': # Tähän loopiin pitää laittaa "updatelocation" funktio (alhaalla oleva), eli Phileasin location päivitty jokaisen vuoron jälkeen
    #print(valikoima())
    #print(etäisyys)
    #print(varmistus)

updatelocation(icao2)
print(icao1)