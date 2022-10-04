import mysql.connector
import math

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

distance = int(input(f'Kuinka monta kilometria haluat lentaa? ')) # kilometreina

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
    print(sql)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

print(valikoima())