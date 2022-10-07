import mysql.connector

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='123',            #pitää olla 1 yhteys koko koodissa ja yksi password, miten se toimi?
         autocommit=True
         )


def onkoAlennusAlue(icao):
    tuple = (icao,)
    sql = '''SELECT latitude_deg FROM airport 
    WHERE ident = %s'''
    kursori = yhteys.cursor()
    kursori.execute(sql, tuple)
    tulos = kursori.fetchone()
    print(tulos)
    if tulos[0] < 40:
        return 0.5
    elif 40 <= tulos[0] <= 60:
        return 1
    elif tulos[0] < 20:
        return 0.7
    else:
        return 1.3


mihin = input(f'Valitse yksi niistä ja matkustetaan seuraavalle lentokentälle. Kirjoita ICAO-koodin:  ')
icao2 = mihin

print(f'Lentokennan {icao2} aluella on alennus {onkoAlennusAlue(icao2)}')