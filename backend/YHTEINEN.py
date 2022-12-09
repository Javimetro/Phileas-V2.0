import mysql.connector
from geopy.distance import geodesic
from geopy import distance
import random
import config


def updatelocation(icao, userId):
    sql = f'''UPDATE game SET location= %s WHERE id={userId}'''
    tuple = (icao,)
    kursori = config.conn.cursor()
    kursori.execute(sql,tuple)


def haelongitude(userId):
    sql = f'''select longitude_deg
    from airport, game
    where game.id={userId} and location = ident'''
    kursori = config.conn.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos


def haelatitude(userId):
    sql = f'''select latitude_deg
    from airport, game
    where game.id={userId} and location = ident'''
    kursori = config.conn.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos


def valikoima(kilometrit, userId):
    lat1=haelatitude(userId)
    lon1=haelongitude(userId)
    northlimit = float(lat1[0]) + float(kilometrit) * 0.01
    southlimit = float(lat1[0]) - float(kilometrit) * 0.01
    westlimit = lon1[0]
    eastlimit = float(lon1[0]) + float(kilometrit) * 0.01
    if southlimit < 0:
        southlimit = 0
    if northlimit > 80:
        northlimit = 80
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
    return tulos


def vaihtoehdot(km, userId):
    vaihtoehdot1 = []

    tulos = valikoima(km, userId)
    for i in range(10):
        vaihtoehdot1.append(random.choice(tulos))
    return vaihtoehdot1


def etaisyysicaolla(icao):
    tuple = (icao,)
    sql = '''SELECT latitude_deg, longitude_deg 
    FROM airport 
    WHERE ident = %s'''
    kursori = config.conn.cursor()
    kursori.execute(sql, tuple)
    tulos = kursori.fetchone()
    return tulos


def phileaslocation(userId):
    sql = f'''select latitude_deg, longitude_deg
    from airport, game
    where game.id={userId} and location = ident'''
    kursori = config.conn.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos


def londoncityairport():
    sql = '''select ident, name, latitude_deg, longitude_deg
        from airport
        where ident = "EGLC"'''
    kursori = config.conn.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos


def city_country(userId):
    sql = f'''select airport.municipality, country.name from airport, country, game 
    where game.id={userId} and  game.location=airport.ident and airport.iso_country=country.iso_country;'''
    kursori = config.conn.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    for i in tulos:
        print(f'{i[0]} ,{i[1]}')


def onkoAlennusAlue(icao):
    tuple = (icao,)
    sql = '''SELECT latitude_deg FROM airport 
    WHERE ident = %s'''
    kursori = config.conn.cursor()
    kursori.execute(sql, tuple)
    tulos = kursori.fetchone()
    if 20 < tulos[0] < 40:
        #print('Olet alennusalueella. Saat 50% alennusta.')
        return 0.5
    elif 40 <= tulos[0] <= 60:
        #print('Matkasi hinta on suoraan verrannollinen kuljettuun matkaan.')
        return 1
    elif 0 < tulos[0] < 20:
        #print('Olet alennusalueella. Saat 70% alennusta.')
        return 0.3
    elif 60 < tulos[0] < 80:
        #print('Olet korkeammalla alueella. Joudut maksamaan 30% enemmän.')
        return 1.3
def etaisyys(icao1,icao2):
    km = round(geodesic(etaisyysicaolla(icao1), etaisyysicaolla(icao2)).km, 3)
    return km

def hintakaava(icao1, icao2):
    km = round(geodesic(etaisyysicaolla(icao1), etaisyysicaolla(icao2)).km, 3)
    hinta = km/10 * onkoAlennusAlue(icao2)
    return hinta


def getInfoById(userId):
    sql = f'''select * from game where game.id={userId}'''
    kursori = config.conn.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos


def lisaraha(hinta):
    raha = hinta * 0.5
    return raha


def aloitusbudjetti(userId):
    sql = f'''UPDATE game SET co2_budget=1000, co2_consumed=0 WHERE id={userId}'''
    kursori = config.conn.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos


def hae_budjetti(userId):
    sql = f'''SELECT co2_budget FROM game WHERE id={userId}'''
    kursori = config.conn.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos[0]


def paivita_budjetti(hinta,raha, userId):
    sql = f'''UPDATE game SET co2_budget=co2_budget-{hinta}+{raha}, co2_consumed=co2_consumed+{hinta} WHERE id={userId}'''
    kursori=config.conn.cursor()
    kursori.execute(sql)
    tulos=kursori.fetchone()
    return tulos


def tarkista_budjetti(userId):
    sql = f'''SELECT co2_budget FROM game WHERE id={userId}'''
    kursori=config.conn.cursor()
    kursori.execute(sql)
    tulos=kursori.fetchone()
    return tulos[0]

# to DB
vuorot = 0
lopullinenbudjetti = 0
# updatelocation('EGLC')
# aloitusbudjetti()
# lat1 = haelatitude()
# lon1 = haelongitude()
# print("Olet maailmankuulu maailmanmatkaaja Phileas Fogg ja sinut on haastettu matkustamaan maailman ympäri niin nopeasti kuin pysyt."
#       "\nLennät maailman ympäri valitsemalla haluamasi matkan pituuden, mutta muista että pideämmät matkat ovat kalliimpia!"
#       "\nAloitat kotoasi Lontoosta ja sinne haluat myös palata voittaaksesi."
#       "\nOnnea matkaan, toivottavasti reisussa kestää tällä kertaa vähemmän kuin 80 päivää!\n")
# # input('-Paina näppäintä ja aloitetaan matka-')
# print(f'Olet nyt London City Airportilla ja koordinaattisi ovat: {lat1[0],lon1[0]}')
# budjetti = hae_budjetti()
# aloitusbudjetti = hae_budjetti()
# print(f"Budjettisi on alussa {budjetti}€. Tämän lisäksi saat joka matkan jälkeen hieman lisärahaa.")
# # input('')
# print('Ennen kuin aloitat matkasi, on tärkeää, että sinulla on tietoa lippujen hinnoista ja niiden suhteesta etäisyyksiin.'
#       "\nMatkasi hinta riippuu leveysasteista, joiden välillä lennät.")
# # input('')
# print('*Leveysasteet 40-60: Matkakustannukset ovat suoraan verrannollisia matkan pituuteen, koska lähtö- ja tulopaikka sijaitsevat tällä alueella.')
# # input('')
# print('*Leveysasteet 20-40: Näillä alueilla matkasi hinta on 30 prosenttia halvempi, mutta matka voi kestää hieman kauemmin.'
#       '\nMaapallon ympärillä oleva matka alkaa pidentyä koska meridiaanien välinen etäisyys on suurempi kuin Lontoossa.')
# input('')
# print('*Leveysasteet 0-20: Täällä liput ovat todella halpoja (70 % alennus!), mutta matka maapallon ympäri on kaikista pisin. Lennät lähellä päiväntasaajaa.')
# input('')
# print('*Leveysasteet 60-80: Tämä alue on lähellä pohjoisnapaa, ja täällä ei kestä kauan lentää maailman ympäri (meridiaanien välinen etäisyys on hyvin pieni). '
#       '\nTästä syystä liput ovat 30 prosenttia kalliimpia.')
# input('')
#
# yht_etaisyys = 0
# while budjetti > 0:
#     kilometrit = int(input(f'Kuinka monta kilometriä haluaisit lentää? '))
#
#     print(f'Sillä etäisyydellä voit matkustaa seuraaville lentokentille:\n')
#     tulos = vaihtoehdot()
#
#     if yht_etaisyys > 5000:
#         lontoo = londoncityairport()
#         etaisyysLCA = distance.distance(phileaslocation(), lontoo[2:])
#         print(f'etäisyys Lontoosta: {etaisyysLCA}\n')
#         if -50 < lon1[0] < 5 and kilometrit >= etaisyysLCA:
#             tulos.append(lontoo)
#
#     i = 1
#     for n in tulos:
#         print(f'{i}: {n}')
#         i = i + 1
#
#     mihin = input(f'\n Valitse niistä yksi ja matkustetaan sille lentokentälle. Kirjoita numero:  ')
#
#     phileaslocation()
#     icao2 = tulos[int(mihin) - 1][0]
#
#     km = round(geodesic(phileaslocation(), etaisyysicaolla(icao2)).km, 3)
#     print(f' Etäisyys lentokenttien välillä on: {km} Km.')
#
#     hinta = hintakaava(km)
#     print(f'Valitulle lentoasemalle lähtevän lennon hinta on {hinta:.2f} €')
#     print(f'Valitusta lennosta saamasi lisäraha on {lisaraha(hinta):.2f} €')
#
#
#     varmistus = input(f'Oletko varma, että haluat matkustaa {icao2} lentokentälle (K/E)?: ')
#     if varmistus == 'K':
#
#         print('')
#         paivita_budjetti(hinta, lisaraha(hinta))
#         budjetti = tarkista_budjetti()
#         if budjetti < 0:
#             print('Upsis! Sinulla ei ole rahaa enää. Peli ohi :(')
#             break
#         updatelocation(icao2)
#         city_country()
#         lat1 = haelatitude()
#         lon1 = haelongitude()
#         print('')
#
#         lopullinenbudjetti = lopullinenbudjetti + hinta
#         yht_etaisyys = yht_etaisyys + km
#         vuorot += 1
#
#         if phileaslocation() == (51.505299, 0.055278):
#             print(f'Onneksi olkoon! Olet päässyt takaisin Lontooseen! \nLensit yhteensä {vuorot} kertaa, kilometrejä kertyi yhteensä {yht_etaisyys} ja käytit {lopullinenbudjetti:.2f}€ verran rahaa')
#             break
#         else:
#             print(f'No niin, nyt sinun koordinaattisi ovat {lat1[0], lon1[0]}, budjettisi on {budjetti:.2f} €')
#     else:
#         print("Oho! Ehkä budjettisi ei riitä... Ei haittaa! Yritetään uudestaan. Valitse uusi vaihtoehto, joka sopii paremmin.")
