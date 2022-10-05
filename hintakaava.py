import mysql.connector

yhteys = mysql.connector.connect(
        host='127.0.0.1',
        port= 3306,
        database='flight_game',
        user='root',
        password='1417',
        autocommit=True
        )

def koordinaatit():
   sql = '''SELECT case when latitude_deg between 40 and 60 then 0 when latitude_deg between 60 and 80 then 1
     when latitude_deg between 20 and 40 then 2 when latitude_deg between 0 and 20 then 3 ELSE 4
     end as alue FROM airport where latitude_deg = 51.505299;'''
   kursori = yhteys.cursor()
   kursori.execute(sql)
   tulos = kursori.fetchone()
   return tulos

def hintakaava(km):
   tulos = koordinaatit()
   if tulos[0] == 0:
       print('Matkasi hinta on suoraan verrannollinen kuljettuun matkaan.')
       hinta = km / 10
   elif tulos[0] == 1:
       print('Olet korkeammalla alueella. Joudut maksamaan 30% enemmän.')
       hinta = km / 10 * 1.3
   elif tulos[0] == 2:
       print('Olet alennusalueella. Saat 50% alennusta.')
       hinta = km / 10 * 0.5
   elif tulos[0] == 3:
       print('Olet alennusalueella. Saat 70% alennusta.')
       hinta = km / 10 * 0.3
   else:
       print('Et voi matkustaa tälle alueelle.')
       km = float(input('Kuinka monta kilometriä haluat kulkea? '))
   return hinta

kilometrit = float(input('Kuinka monta kilometriä haluat matkustaa? '))
print(f'Matkan hinnaksi tulee {hintakaava(kilometrit)}€')


#40<latitude<60 = normaali
#60<latitude<80 = eka (kalliimpi)
#20<latitude<40 = toka (eka alennusalue)
#0<latitude<20 = kolmas (toka alennusalue)
#else liian korkea/matala