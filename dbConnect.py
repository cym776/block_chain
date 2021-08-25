# 导入模块
import pymysql
from time import time

host = 'localhost'
port = 3306
user = 'root'
passwd = '123'
datebase = 'time_bank'


def insertBill(index, time, sender, receiver, account, detail, block_id):
    # 打开数据库连接
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=datebase, charset='utf8')
    # 使用cursor方法创建一个游标
    cursor = db.cursor()
    try:
        # 插入交易记录
        cursor.execute(
            "insert into bill(index_num, sender, receiver, account, detail, time, block_id) values({0}, '{1}', '{2}', '{3}', '{4}', '{5}', {6})".format(
                index, sender, receiver, account, detail, time, block_id))
        # 更新账户信息
        cursor.execute("update user set account=account-{0} where name='{1}'".format(account, sender))
        cursor.execute("update user set account={0}+account where name='{1}'".format(account, receiver))
        # 提交修改
        db.commit()
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


def insertBlock(block):
    # 打开数据库连接
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=datebase, charset='utf8')
    # 使用cursor方法创建一个游标
    cursor = db.cursor()
    try:
        # 插入交易记录
        cursor.execute(
            "insert into block(`index`, time, proof, previous_hash) values({0}, '{1}', '{2}', '{3}')".format(
                block['index'], block['time'], block['proof'], block['previous_hash']))
        # 提交修改
        db.commit()
    except Exception as e:
        print("error : " + e)
        # 发生错误时回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


def getIndex():
    # 打开数据库连接
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=datebase, charset='utf8')
    # 使用cursor方法创建一个游标
    cursor = db.cursor()
    try:
        # 执行 SQL 语句
        cursor.execute("select * from block order by id DESC limit 1")
        data = cursor.fetchone()
        # print(data[1])
        # 提交修改
        db.commit()
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
    # 关闭数据库连接
    db.close()

    if data is None:
        return -1
    else:
        return data[1]


def getLastBlock():
    # 打开数据库连接
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=datebase, charset='utf8')
    # 使用cursor方法创建一个游标
    cursor = db.cursor()
    try:
        # 执行 SQL 语句
        cursor.execute("select * from block order by id DESC limit 1")
        data = cursor.fetchone()
        index = str(data[1])

        cursor.execute("select * from bill where block_id=" + index)
        trans_data = cursor.fetchall()

        list_data = list(trans_data)
        dict_array = []
        for i in list_data:
            dict1 = {"time": i[2], "sender": i[3], "receiver": i[4], "account": i[5], "detail": i[6]}
            dict_array.append(dict1)
        # 提交修改
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    # 关闭数据库连接
    db.close()

    block = {
        'index': data[1],
        'time': data[2],
        'transactions': dict_array,
        'proof': data[3],
        'previous_hash': data[4],
    }
    return block


# db = pymysql.connect(host='192.168.1.237', port=3306, user='root', passwd='123', db='time_bank', charset='utf8')
# cursor = db.cursor()
# cursor.execute("select * from bill order by id DESC limit 1")
# data = cursor.fetchone()
# print(data)
