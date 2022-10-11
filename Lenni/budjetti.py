import mysql.connector
yhteys =mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='my_game',
         user='root',
         password='Torstai22#',
         autocommit=True
         )
#nämä ovat placeholdereita kokeiluja varten
budjetti_1=1000
matkakustannus=700
alennus=500
peli_id=2
print(f'Sinut on haastettu matkaamaan maailman ympäri. Hyvää onnea!')

#Testaan aluksi että budjetin päivitys tietokantaan onnistui

def hae_budjetti():
    sql=f'''SELECT co2_budget FROM game WHERE id={peli_id} '''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos
print(f"Budjettisi on alussa {hae_budjetti()}. Tämän lisäksi saat joka matkan jälkeen hieman lisärahaa.")


def paivita_budjetti(alennus,matkakustannus):

    sql=f'''UPDATE game SET co2_budget=co2_budget+{alennus}-{matkakustannus} WHERE id={peli_id}'''
    print(sql)
    kursori=yhteys.cursor()
    kursori.execute(sql)
    tulos=kursori.fetchone()
    return tulos

def tarkista_budjetti():
    sql=f'''SELECT screen_name FROM game WHERE id={peli_id} AND co2_budget<=0'''
    print(sql)
    kursori=yhteys.cursor()
    kursori.execute(sql)
    tulos=kursori.fetchall()
    return tulos



if len(tarkista_budjetti())>0:
    print("Peli ohi")
