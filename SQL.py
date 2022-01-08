import pymysql

connection = pymysql.connect(db="hubobel",
                             user="hubobel",
                             passwd="polier2003",
                             host='10.0.1.123', charset='utf8')
cursor = connection.cursor()
try:
    cursor.execute("""CREATE TABLE speedTest ( 
        nr INT, timestamp TEXT,server TEXT,ip TEXT, ping FLOAT, download FLOAT, upload FLOAT)""")
except:
    print('weiter')


def Prognose():

    try:
        down7 = 0
        down1 = 0
        down24 = 0
        sql = "SELECT Nr FROM speedTest"
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
        sql = "SELECT * FROM speedTest ORDER BY Nr DESC LIMIT " + str(t1)  # ASC
        cursor.execute(sql)
        resp = cursor.fetchall()
        for i in resp:
            down1 = down1 + int(i[5])
        down1 = round(down1 / (t1), 2)
        # 7 Tage
        sql = "SELECT * FROM speedTest ORDER BY Nr DESC LIMIT " + str(t7)  # ASC
        cursor.execute(sql)
        resp = cursor.fetchall()
        for i in resp:
            down7 = down7 + int(i[5])
        down7 = round(down7 / (t7), 2)
        # 24 Tage
        sql = "SELECT * FROM speedTest ORDER BY Nr DESC LIMIT " + str(t24)  # ASC
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


down1, down7, down24 = Prognose()

print(down1, down7, down24)
cursor.close()
connection.close()
