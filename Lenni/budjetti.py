import mysql.connector
yhteys =mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='my_game',
         user='root',
         password='Torstai22#',
         autocommit=True
         )

budjetti_1=1000
matkakustannus=700
alennus=500
print(f'Sinut on haastettu matkaamaan maailman ympäri. Hyvää onnea!')

#Testaan aluksi että budjetin päivitys tietokantaan onnistui

def hae_budjetti():
    sql=f'''SELECT co2_budget FROM game'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos
print(f"Budjettisi on alussa {hae_budjetti()}. Tämän lisäksi saat joka matkan jälkeen hieman lisärahaa")

def paivita_budjetti():
    budjetti=1000
    sql="UPDATE game SET co2_budget="+str(budjetti)
    print(sql)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos=kursori.fetchone()
    return