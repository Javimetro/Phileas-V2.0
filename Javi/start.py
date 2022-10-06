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

print(f' Hei Phileas! Nyt olet London City Airportissa ja sinun kordinaatit ovat: {lat1[0],lon1[0]}')

distance = int(input(f'Kuinka monta kilometria haluaisit sinun ekällä matkalla lentää? ')) # kilometreina

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

print(f' Silla etäisyydellä voit matkustaa seuraville lentokentalle: {valikoima()}')


mihin = input(f'Valitse yksi niistä ja matkustetaan seuraavalle lentokentälle. Kirjoita ICAO-koodin:  ')

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


icao2 = mihin

etäisyys = print(f' Etäisyys lentokenttien välillä on: {round(geodesic(phileaslocation(), etaisyysicaolla(icao2)).km,3)} Km.')
varmistus = input(f'Oletko varma haluatko matkustaa {mihin} ICAO-koodinen lentokentälle (K/E)?: ')

#while varmistus == 'K': # Tähän loopiin pitää laittaa "updatelocation" funktio (alhaalla oleva), eli se location päivitty jokaisen vuoron jälkeen
    #print(valikoima())
    #print(etäisyys)
    #print(varmistus)

#def updatelocation(): #Tämä ei vielä toimi, pitää päivittää database.
    #sql = '''UPDATE game SET location =''' icao2
    #print(sql)
    #kursori = yhteys.cursor()
    #kursori.execute(sql)
    #if kursori.rowcount == 1:
        #print("Location päivitetty")
