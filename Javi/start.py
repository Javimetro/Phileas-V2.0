import mysql.connector
from geopy.distance import geodesic

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

lat1 = haelatitude()
lon1 = haelongitude()

distance = int(input(f'Kuinka monta kilometria haluat lentää? ')) # kilometreina

northlimit = lat1[0] + distance*0.01
southlimit = lat1[0] - distance*0.01
westlimit = lon1[0] + distance*0.01
eastlimit = lon1[0] - distance*0.01

print(f' London City Airport kordinaatit ovat: {lat1[0],lon1[0]}')
print(f' North limit on: {northlimit}, south limit on: {southlimit},west limit on: {westlimit},east limit on: {eastlimit}')

def valikoima():
    sql = f'''SELECT ident, name, latitude_deg, longitude_deg
    FROM Airport WHERE latitude_deg BETWEEN {southlimit} AND {northlimit}
    AND longitude_deg BETWEEN {eastlimit} AND {westlimit}'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

print(valikoima())


mihin = input(f'Mihin haluaisit lentää seuraavaksi? (Kirjoita lentokentän ICAO-koodin) ')

def etaisyysicaolla(icao):
    tuple = (icao,)
    sql = '''SELECT latitude_deg, longitude_deg 
    FROM airport 
    WHERE ident = %s'''
    kursori = yhteys.cursor()
    kursori.execute(sql, tuple)
    tulos = kursori.fetchone()
    print(tulos)
    return tulos

icao1 = 'EGLC'
icao2 = mihin

etäisyys = print(f' Etäisyys lentokenttien välillä on: {round(geodesic(etaisyysicaolla(icao1), etaisyysicaolla(icao2)).km,3)} Km.')
varmistus = input(f'Oletko varma haluatko matkustaa {mihin} ICAO-koodinen lentokentälle (K/E)?: ')

while varmistus == 'K': # Tähän loopiin pitää laittaa "updatelocation" funktio (alhaalla oleva), eli se location päivitty jokaisen vuoron jälkeen
    distance = int(input(f'Kuinka monta kilometria haluat lentää? '))
    print(valikoima())
    print(etäisyys)
    print(varmistus)

def updatelocation(): #Tämä ei vielä toimi, pitää päivittää database.
    sql = '''UPDATE game SET location =''' icao2
    print(sql)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    if kursori.rowcount == 1:
        print("Location päivitetty")
