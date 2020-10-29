#!/usr/local/python3

from datetime import datetime
from decimal import Decimal

from pymysqlpool import ConnectionPool

from autotest.utils import ObjDict


def connection_pool(config):
    return ConnectionPool(**config)


def type_convert(rs, is_assert):
    for i, row in enumerate(rs):
        for k, v in row.items():
            if isinstance(v, datetime):
                rs[i].update({k: str(v)})
            elif isinstance(v, Decimal):
                rs[i].update({k: float(v)})
            else:
                pass
    for i, row in enumerate(rs):
        if isinstance(row, dict):
            rs[i] = ObjDict(row)

    if is_assert:
        return list(rs)

    if not rs:  # 结果集为空
        return None
    elif len(rs[0]) == 1:  # 查询列只有一个字段
        if len(rs) == 1:  # 只有一条记录
            return list(rs[0].values())[0]
        else:
            for i, v in enumerate(rs):
                rs[i] = list(rs[i].values())[0]
            return list(rs)
    else:
        return list(rs)


class MysqlSampler:
    def __init__(self, conn_dict):
        self.pool = connection_pool(conn_dict)

    def execute(self, sql, is_assert=False):
        with self.pool.connection() as conn:
            cursor = conn.cursor()
            result = cursor.execute(sql)
            conn.commit()
            if sql.strip().lower().startswith("select"):
                return type_convert(cursor.fetchall(), is_assert)
            else:
                return result

    def execute_many(self, sql, params):
        with self.pool.connection() as conn:
            cursor = conn.cursor()
            result = cursor.executemany(sql, params)
            conn.commit()
            return result


class MysqlSamplerOld:
    def __init__(self, conn_dict):
        self.cursor = connection_pool(conn_dict).cursor()

    def execute(self, sql, is_assert=False):
        with self.cursor as cursor:
            result = cursor.execute(sql)
            if sql.strip().lower().startswith("select"):
                return type_convert(cursor.fetchall(), is_assert)
            else:
                return result

    def execute_many(self, sql, params):
        with self.cursor as cursor:
            result = cursor.executemany(sql, params)
            return result


if __name__ == "__main__":
    import random
    import time
    # s = "select * from comm_area limit %s, %s"
    # s2 = "select ID, name from comm_area where 1=2"
    # s3 = "SELECT STATUS FROM t_apply_msg  -- WHERE  request_number ='6d2d1d27-1ece-480e-ab56-79fd53682e43'"
    conn = {
        "host": "39.100.114.133", "port": 4000, "user": "admin", "password": "testadminds2019",
        "database": "stay", "pool_name": "test"
    }
    
    # ss = "SELECT *  FROM stay.app_game_ticket where user_id = '5499' "
    sam = MysqlSampler(conn)
    # # r = sam.execute(s)
    # p = [[1, 2], [2, 5]]
    # # r = sam.execute_many(s, p)
    # r = sam.execute(ss)
    #
    
    #
    # update_sql = "UPDATE `app_game_ticket` SET `count`=5 WHERE `count` != 5 "
    #
    # select_sql = "select count(1) from  app_game_ticket where count=0 "
    #
    # while True:
    #     aa = sam.execute(select_sql)
    #     if aa == 0:
    #         break
    #     else:
    #         a = time.time()
    #         sam.execute(update_sql)
    #         b = time.time()
    #         print("执行耗时：", b-a)
    # for i in range(1, 20):
    #
    #     sql = "insert into stay.app_game_ticket(count, user_id, subscribe_match, lucky_score, createdAt, updatedAt) " \
    #           "values (0, %s, 0, 0, '2019-10-08 00:00:00', '2019-10-08 00:00:00' )"
    #     param_list = []
    #     for j in range(1, 1000):
    #         print("开始准备第 {} 批次数量插入".format(str(i)))
    #         param_list.append(((str(i) + str(random.randint(10000, 1000000)),)))
    #     print("开始插入数据插入数据")
    #     sam.execute_many(sql, param_list)
