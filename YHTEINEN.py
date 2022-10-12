import mysql.connector
from geopy.distance import geodesic
from geopy import distance
import random

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port=3306,
         database='flight_game',
         user='root',
         password='1417',
         autocommit=True
         )

# poistettiin rivin 'print'
def updatelocation(icao):
    sql = '''UPDATE game SET location= %s WHERE screen_name = "Phileas Fogg"'''
    tuple = (icao,)
    kursori = yhteys.cursor()
    kursori.execute(sql,tuple)
    if kursori.rowcount == 1:
        print("LOCATION UPDATED")


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

# Siirrettiin limits funktioon, koska niitä tarvitaan vain funktiossa eikä niitä käytetä missään muualla.
# Lisättiin myös rajat funktioon, nyt se toimi
def valikoima():
    northlimit = lat1[0] + kilometrit * 0.01
    southlimit = lat1[0] - kilometrit * 0.01
    westlimit = lon1[0]
    eastlimit = lon1[0] + kilometrit * 0.01
    if southlimit < 0:
        southlimit = 0
    if northlimit > 80:
        northlimit = 80
    if -180 < eastlimit < 180:
        sql = f'''SELECT ident, name, latitude_deg, longitude_deg
            FROM Airport WHERE latitude_deg BETWEEN {southlimit} AND {northlimit}
            AND longitude_deg BETWEEN {westlimit} AND {eastlimit}'''
    elif eastlimit > 180:
        eastlimit = eastlimit - 360

        sql = f'''SELECT ident, name, latitude_deg, longitude_deg
            FROM Airport WHERE latitude_deg BETWEEN {southlimit} AND {northlimit}
            AND longitude_deg BETWEEN {-180} AND {eastlimit} AND {westlimit} AND {180}'''

    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos


def vaihtoehdot():
    vaihtoehdot1 = []
    tulos = valikoima()
    for i in range(4):
        vaihtoehdot1.append(random.choice(tulos))
    return vaihtoehdot1



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

def londoncityairport():
    sql = '''select latitude_deg, longitude_deg
        from airport
        where ident = "EGLC"'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos

def onkoAlennusAlue(icao):
    tuple = (icao,)
    sql = '''SELECT latitude_deg FROM airport 
    WHERE ident = %s'''
    kursori = yhteys.cursor()
    kursori.execute(sql, tuple)
    tulos = kursori.fetchone()
    if 20 < tulos[0] < 40:
        print('Olet alennusalueella. Saat 50% alennusta.')
        return 0.5
    elif 40 <= tulos[0] <= 60:
        print('Matkasi hinta on suoraan verrannollinen kuljettuun matkaan.')
        return 1
    elif 0 < tulos[0] < 20:
        print('Olet alennusalueella. Saat 70% alennusta.')
        return 0.3
    elif 60 < tulos[0] < 80:
        print('Olet korkeammalla alueella. Joudut maksamaan 30% enemmän.')
        return 1.3


def hintakaava(km):
    hinta = km/10 * onkoAlennusAlue(icao2)
    return hinta


def lisaraha(hinta):
    raha = hinta * 0.7
    return raha


def hae_budjetti():
    sql = f'''SELECT co2_budget FROM game'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos[0]


def paivita_budjetti(hinta,raha):

    sql = f'''UPDATE game SET co2_budget=co2_budget-{hinta}+{raha} WHERE id=1'''
    kursori=yhteys.cursor()
    kursori.execute(sql)
    tulos=kursori.fetchone()
    return tulos


def tarkista_budjetti():
    sql = f'''SELECT co2_budget FROM game WHERE id=1'''
    kursori=yhteys.cursor()
    kursori.execute(sql)
    tulos=kursori.fetchone()
    return tulos[0]



# Siirettiin kaikki funktiot ylös ja toiminnot alas

updatelocation('EGLC')
lat1 = haelatitude()
lon1 = haelongitude()
print(f'Hei Phileas! Olet nyt London City Airportilla ja koordinaattisi ovat: {lat1[0],lon1[0]}')
budjetti = hae_budjetti()
print(f"Budjettisi on alussa {budjetti}€. Tämän lisäksi saat joka matkan jälkeen hieman lisärahaa.")


while budjetti > 0:
    kilometrit = int(input(f'Kuinka monta kilometriä haluaisit lentää? '))

    etaisyysLCA = distance.distance(phileaslocation(), londoncityairport())
    print(f'etäisyys londonCA: {etaisyysLCA}')
    if kilometrit >= etaisyysLCA:
        varmistus = input('Voit matkustaa takaisin London City Airportiin. Haluatko palata sinne? (K/E): ')
        if varmistus == 'K':
            updatelocation('EGLC')
            break

    print(f'Sillä etäisyydellä voit matkustaa seuraaville lentokentille:\n')
    tulos = vaihtoehdot()
    i = 1
    for n in tulos:
        print(f'{i}: {n}')
        i = i + 1
    mihin = input(f'\n Valitse niistä yksi ja matkustetaan sille lentokentälle. Kirjoita numero:  ')

    phileaslocation()
    icao2 = tulos[int(mihin) - 1][0]

    km = round(geodesic(phileaslocation(), etaisyysicaolla(icao2)).km, 3)
    print(f' Etäisyys lentokenttien välillä on: {km} Km.')

    hinta = hintakaava(km)
    print(f'Valitulle lentoasemalle lähtevän lennon hinta on {hinta:.2f} €')

    varmistus = input(f'Oletko varma, että haluat matkustaa {mihin} lentokentälle (K/E)?: ')
    if varmistus == 'K' and budjetti > hinta:
        updatelocation(icao2)
        lat1 = haelatitude()
        lon1 = haelongitude()
        paivita_budjetti(hinta, lisaraha(hinta))
        budjetti = tarkista_budjetti()

        # budget calc from Lenni
        # budjetti = budjetti - hinta
        # Pitää kirjoittaa jotain kaunista
        print(f'No niin, nyt sinun koordinaattisi ovat {lat1[0], lon1[0]}, budjettisi on {budjetti:.2f} €')
    else:
        print("Oho! Ehkä budjettisi ei riitä... Ei haittaa! Yritetään uudestaan. Valitse uusi vaihtoehto, joka sopii paremmin.")

if phileaslocation() == (51.505299, 0.055278):
    print('Onneksi olkoon! Olet päässyt takaisin Lontooseen!')