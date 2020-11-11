#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Created by Eason on 2019/8/15.

import urllib3
from requests import *
import pymysql
from pymysql import *
import sqlite3
import random


#name = input("请输入姓名：")
conn = pymysql.connect(host='39.100.228.129', port=4000,user='admin',password='testadminds2019',database='stay',charset='utf8')
cursor = conn.cursor()
# sql1 = 'select * FROM app_treasure_detail;'
# sql2 = 'select * FROM app_user_treasure;'
sql3 = 'select * FROM app_live_perm ;'
sql4 = 'insert INTO app_live_perm(id,name,gender) VALUES (%s,%s,%s);'
for i in range(10000):
    data = [(str(i)+"@qq.com","c4ca4238a0b923820dcc509a6f75849b","http://static.rela.me/app/avatar/106759836/c9ffb3f218faf6ca873fdc9a4b01f722.jpg","test","2222")]
    sql5 = 'insert INTO app_user(`email`,`password`, `avatar`, `nickName`,`user_name`) VALUES (%s,%s,%s,%s,%s);'
    cursor.executemany(sql5,data)
    conn.commit()

cursor.close()
conn.close()

# String sql = "INSERT INTO location(longitude, latitude)" + " VALUES (“+mylongitude+","+mylatitude+")"
# for i in range(2):
#     cursor.execute(sql5)
#     i+=1
#     cursor.close()
#     conn.close()


# sql2 = 'select * FROM mytable WHERE name=%s;'
# # sql3 = 'insert INTO bb(id,name,gender) VALUES (%s,%s,%s);'
# # sql4 = 'delete from bb where id = %s;'
# # sql5 = 'update bb SET  gender = %s where id = %s;'
# # sql6 = 'select * from bb where id = 3;'

# cursor.execute(sql6)
# # ret = cursor.fetchall()
# cursor.close()
# conn.close()
# print(ret)
'''
conn = pymysql.connect(host='39.100.228.129',port=4000,user='admin',password='testadminds2019',database='livedb',charset='utf8')
cursor = conn.cursor()
# sql1 = 'select * FROM app_treasure_detail;'
# sql2 = 'select * FROM app_user_treasure;'
# sql3 = 'select * FROM app_live_perm ;'
# sql4 = 'insert INTO app_live_perm(id,name,gender) VALUES (%s,%s,%s);'
for i in range(1000):
    data = [(i+106789975,2,"autotest",450301199007176365)]
    sql5 = 'insert INTO app_live_perm(`id`,`perm`, `real_name`, `id_number`) VALUES (%s,%s,%s,%s);'
    cursor.executemany(sql5,data)
    conn.commit()

cursor.close()
conn.close()
'''

'''
conn = pymysql.connect(host='39.100.228.129',port=4000,user='admin',password='testadminds2019',database='livedb',charset='utf8')
cursor = conn.cursor()
# sql1 = 'select * FROM app_treasure_detail;'
# sql2 = 'select * FROM app_user_treasure;'
# sql3 = 'select * FROM app_live_perm ;'
# sql4 = 'insert INTO app_live_perm(id,name,gender) VALUES (%s,%s,%s);'

for i in range(100):
    data = [(i+106789977,1000000.0000)]
    sql5 = 'INSERT INTO `app_user_treasure` (`id`,`gold`) VALUES (%s,%s);'
    try:
        cursor.executemany(sql5, data)
        conn.commit()
    except IntegrityError as e:
            pass
    continue
cursor.close()
conn.close()



conn = pymysql.connect(host='39.100.228.129',port=4000,user='admin',password='testadminds2019',database='backend',charset='utf8')
cursor = conn.cursor()
# sql1 = 'select * FROM app_treasure_detail;'
# sql2 = 'select * FROM app_user_treasure;'
# sql3 = 'select * FROM app_live_perm ;'
# sql4 = 'insert INTO app_live_perm(id,name,gender) VALUES (%s,%s,%s);'
userid = 106789900
str1 = '哈哈'
for i in range(2000):
    data = [('2019-11-29', i+userid, 310100, 1, 0, '哈哈')]
    sql5 = 'insert INTO web_game_stars_mood((`sameday`, `userId`, `city`, `mood`, `anonymous`, `content`)VALUES (%s,%s,%s,%s,%s,%s);'
    cursor.executemany(sql5, data)
    conn.commit()
cursor.close()
conn.close()



import requests
import json
import ssl
str1 = '测试'
import os
import sys
list1 = range(2000)
list2 = []
for i in list1:
    list2.append(i+106789910)
url1 = 'https://test-web-api.rela.me/game/stars/sendFlyingMood'

headers = {
    'Date':'Fri, 29 Nov 2019 06:18:18 GMT',
    'Content-Type':'application/json; charset=utf-8',
    'Content-Length':'231',
    'Connection':'keep-alive',
    'Access-Control-Allow-Methods':'GET,HEAD,PUT,POST,DELETE',
    'Vary':'Accept-Encoding',
    'Strict-Transport-Security':'max-age=15724800; includeSubDomains'

}

for i in [106789910,106789911]:
    data = {
        'userId': i,
        'content': "cs",
        'city': 110100,
        'mood': 1,
        'anonymous': 0}

    try:
        for j in range(5):
            r = requests.post(url=url1, data=data,headers=headers)
    except OSError as e:
        pass
    continue

    # result = r.text
    # assert r.status_code == 200
    # print(json.dumps(result))
'''