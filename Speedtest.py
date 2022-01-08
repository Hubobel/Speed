import speedtest
import pymysql
import time
import random

###################

version = "1.2"
db = 'speedTest'
#db = "speed"
##################

connection = pymysql.connect(db="hubobel",
                             user="hubobel",
                             passwd="polier2003",
                             host='10.0.1.123', charset='utf8')
cursor = connection.cursor()
try:
    cursor.execute("""CREATE TABLE speed ( 
        nr INT, timestamp TEXT,server TEXT,ip TEXT, ping FLOAT, download FLOAT, upload FLOAT, Version TEXT)""")
except:
    print('weiter')

sql = "SELECT * FROM "+db+" ORDER BY Nr DESC"
Anzahl = cursor.execute(sql)
Anzahl = int(Anzahl + 1)

servers = []
threads = None


def test():
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    s.results.share()

    # results_dict = {'client': {'rating': '0', 'loggedin': '0', 'isprating': '3.7', 'ispdlavg': '0', 'ip': '84.63.254.177', 'isp': 'Vodafone Germany DSL', 'lon': '8.1189', 'ispulavg': '0', 'country': 'DE', 'lat': '49.7403'}, 'bytes_sent': 22970368, 'download': 28727296.703763857, 'timestamp': '2022-01-02T15:26:51.753501Z', 'share': u'http://www.speedtest.net/result/12547122848.png', 'bytes_received': 36013552, 'ping': 15.811, 'upload': 17662540.706131537, 'server': {'latency': 15.811, 'name': 'Frankfurt', 'url': 'http://speedtest.ropa.de:8080/speedtest/upload.php', 'country': 'Germany', 'lon': '8.6821', 'cc': 'DE', 'host': 'speedtest.ropa.de:8080', 'sponsor': 'ropa GmbH & Co. KG', 'lat': '50.1109', 'id': '37748', 'd': 57.65047622507195}}

    results_dict = s.results.dict()
    up = float(results_dict['upload']) / 1000000
    ping = float(results_dict['ping'])
    down = float(results_dict['download']) / 1000000
    ip = str(results_dict['client']['ip'])
    server = str(results_dict['server']['url'])
    down = round(down, 2)
    up = round(up, 2)
    ping = round(ping, 1)

    print(down)
    return up, ping, down, ip, server


def schreiben():
    val = f'"{Anzahl}", "{time}", "{server}", "{ip}", "{ping}", "{down}", "{up}", "{version}"'
    sql = f'INSERT INTO speed VALUE ({val})'
    return None

def Prognose():

    try:
        down7 = 0
        down1 = 0
        down24 = 0
        sql = "SELECT Nr FROM "+db
        cursor.execute(sql)
        resp = cursor.fetchall()
        anzahl = int(len(resp))
        tage = int(anzahl / 24)
        if tage < 7:
            t7 = anzahl
        else:
            t7 = 7 * 24
        if tage < 24:
            t24 = anzahl
        else:
            t24 = 24 * 24
        if tage < 1:
            t1 = anzahl
        else:
            t1 = 1 * 24
        # 1 Tag
        sql = "SELECT * FROM "+db+" ORDER BY Nr DESC LIMIT " + str(t1)  # ASC
        cursor.execute(sql)
        resp = cursor.fetchall()
        for i in resp:
            down1 = down1 + int(i[5])
        down1 = round(down1 / (t1), 2)
        # 7 Tage
        sql = "SELECT * FROM "+db+" ORDER BY Nr DESC LIMIT " + str(t7)  # ASC
        cursor.execute(sql)
        resp = cursor.fetchall()
        for i in resp:
            down7 = down7 + int(i[5])
        down7 = round(down7 / (t7), 2)
        # 24 Tage
        sql = "SELECT * FROM "+db+" ORDER BY Nr DESC LIMIT " + str(t24)  # ASC
        cursor.execute(sql)
        resp = cursor.fetchall()
        for i in resp:
            down24 = down24 + int(i[5])
        down24 = round(down24 / t24, 2)
        return down1, down7, down24
    except:
        down1 = 0
        down7 = 0
        down24 = 0
        return down1, down7, down24

i = 24*7
#time = (time.strftime("%Y-%m-%d-%H.%M.%S"))
while i > 0:
    down1, down7, down24 = Prognose()
    zeit = (time.strftime("%Y-%m-%d-%H.%M.%S"))
    print(zeit)
    print(down1, down7, down24)



    server = "hubobel.de" + str(random.randint(0, 300))
    ping = random.randint(0, 300)
    ip = "0.0.0.0"
    down = random.randint(10, 100)
    up = random.randint(0, 30)
    #up, ping, down, ip, server, = test()

    print(zeit)
    val = f'"{Anzahl}", "{zeit}", "{server}", "{ip}", "{ping}", "{down}", "{up}","{down1}","{down7}", "{version}"'
    sql = f'INSERT INTO '+db+f' VALUE ({val})'


    resp = cursor.execute(sql)
    connection.commit()
    print(i)
    i = i -1
    time.sleep(1)


cursor.close()
connection.close()
