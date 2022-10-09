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

def updatelocation(icao):
    sql = '''UPDATE game SET location= %s WHERE screen_name = "Phileas Fogg"'''
    tuple = (icao,)
    print(sql, tuple)
    kursori = yhteys.cursor()
    kursori.execute(sql,tuple)
    if kursori.rowcount == 1:
        print("LOCATION UPDATED")

updatelocation('EGLC')

def haelongitude():
    sql = '''select longitude_deg
    from airport, game
    where screen_name = "Phileas Fogg" and location = ident'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos

def haelatitude():
    sql = '''select latitude_deg
    from airport, game
    where screen_name = "Phileas Fogg" and location = ident'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos



lat1 = haelatitude()
lon1 = haelongitude()

print(f'Hei Phileas! Nyt olet London City Airportilla ja koordinaattisi ovat: {lat1[0],lon1[0]}')
distance = int(input(f'Kuinka monta kilometria haluaisit lentää ekalla matkallasi? '))

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

phileaslocation()
icao2 = mihin

etäisyys = print(f' Etäisyys lentokenttien välillä on: {round(geodesic(phileaslocation(), etaisyysicaolla(icao2)).km,3)} Km.')
varmistus = input(f'Oletko varma, että haluat matkustaa {mihin} lentokentälle (K/E)?: ')

while True: # 'While' Ei ole vielä valmis. ehkä 'for' toimii paremmin. Ongelmia saada 'etäisyys' toimimaan hyvin. Luulen että käyttää aina EGLC icao ykkösenä.
    if varmistus == 'K':
        updatelocation(icao2)
        print(f'Hienoa! Matka on suoritettu ja nyt sinun koordinaattisi ovat: {phileaslocation()}')
        distance = int(input(f'Kuinka monta kilometria haluaisit lentää seuraavalla matkallasi? '))
        print(f'Sillä etäisyydellä voit matkustaa seuraaville lentokentille: {vaihtoehdot()}')
        mihin = input(f'Valitse yksi niistä ja matkustetaan sille lentokentälle. Kirjoita ICAO-koodi:  ')
        phileaslocation()
        icao2 = mihin
        etäisyys = print(f' Etäisyys lentokenttien välillä on: {round(geodesic(phileaslocation(), etaisyysicaolla(icao2)).km,3)} Km.')
    else:
        print(f'Eikö raha riitä? Ei hätää, minä voin tarjota sinulle uusia vaihtoehtoja. Valitse uudestaan, ehkä löydät jotain edullisempaa.')
        distance = int(input(f'Kuinka monta kilometria haluaisit lentää seuraavalla matkallasi? '))
        print(f'Sillä etäisyydellä voit matkustaa seuraaville lentokentille: {vaihtoehdot()}')
        mihin = input(f'Valitse yksi niistä ja matkustetaan sille lentokentälle. Kirjoita ICAO-koodi:  ')
        phileaslocation()
        icao2 = mihin
        etäisyys = print(
            f' Etäisyys lentokenttien välillä on: {round(geodesic(phileaslocation(), etaisyysicaolla(icao2)).km, 3)} Km.')
    varmistus = input(f'Oletko varma, että haluat matkustaa {mihin} lentokentälle (K/E)?: ')