#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql import *


conn = pymysql.connect(host='pc-8vbl25i85y93w1ml9.rwlb.zhangbei.rds.aliyuncs.com', port=3306, user='stayadm', password='7f2cJCfe%d0b9f4d', database='stay', charset='utf8')
cursor = conn.cursor()
# sql1 = 'select * FROM app_treasure_detail;'
# sql2 = 'select * FROM app_user_treasure;'
sql3 = 'select * FROM app_user_follower ;'
sql4 = 'insert INTO app_live_perm(id,name,gender) VALUES (%s,%s,%s);'
sql5 = 'INSERT INTO `app_user_follower` (`user_id`,`follower_id`) VALUES (%s,106759214,);'

for i in range(10000):
        data = [i, 106759214]
        sql6 = 'INSERT INTO `app_user_follower` (`user_id`,`follower_id`) VALUES (%s,%s);'
        cursor.executemany(sql6, data)
        conn.commit()
cursor.close()
conn.close()