import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from snownlp import SnowNLP

# 读取skus表


def read_skuinfo():
    try:
        # 建立连接
        conn = pymysql.connect(
            host='192.168.0.5',
            user='root',
            password='MySQL5.7',
            database='test',
            port=3306,
        )
        # 创建游标
        cursor = conn.cursor()

        sql = "SELECT * FROM index_skus"
        cursor.execute(sql)
        skus = pd.read_sql(sql, conn)
    finally:
        cursor.close()
        conn.close()

    return skus

# 修正sku名称，去掉营销前缀
# sku描述去掉控制符


def nomalize_skus(df):
    skus = df

    # 包含'：'为营销前缀
    prefix = "："
    skuname = skus['skuname']
    skuname = skuname.str.split(prefix).str[-1].str.strip()

    skus.drop(['skuname'], axis=1, inplace=True)
    skus.insert(2, 'skuname', skuname)

    # 删除控制字符
    desc = skus['skudescription']
    desc = desc.str.replace(r'<p>', '')
    desc = desc.str.replace(r'</p>', r'\n')
    desc = desc.str.replace(r'<br>', '')
    desc = desc.str.replace(r'<p.+?>', '')
    desc = desc.str.replace(r'<a.+?>', '')
    desc = desc.str.replace(r'</a>', '')

    skus.drop(['skudescription'], axis=1, inplace=True)
    skus.insert(6, 'skudescription', desc)

    # skus.to_excel('skus.xlsx')
    return skus

# 更新skus表


def updateskus(df):
    skus = df

    user = 'root'
    password = 'MySQL5.7'
    host = '192.168.0.5'
    port = 3306
    database = 'test'

    engine = create_engine(
        f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4')
    conn = engine.connect()  # 创建连接
    skus.to_sql(name='index_skus', con=conn, if_exists='replace', index=False)

# 读取comments表


def read_comments():
    try:
        # 建立连接
        conn = pymysql.connect(
            host='192.168.0.5',
            user='root',
            password='MySQL5.7',
            database='test',
            port=3306,
        )
        # 创建游标
        cursor = conn.cursor()

        sql = "SELECT * FROM index_comments"
        cursor.execute(sql)
        comments = pd.read_sql(sql, conn)
    finally:
        cursor.close()
        conn.close()

    return comments


# 删除空白的评论


def nomalize_comments(df):
    comments = df

    newcomments = comments.drop(comments[comments['cdescription'] == ''].index)

    # newcomments.to_csv('comm.csv')
    return newcomments

# 更新comments表


def updatecomments(df):
    comments = df

    user = 'root'
    password = 'MySQL5.7'
    host = '192.168.0.5'
    port = 3306
    database = 'test'

    engine = create_engine(
        f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4')
    conn = engine.connect()  # 创建连接
    comments.to_sql(name='index_comments', con=conn,
                    if_exists='replace', index=False)


# 生成情感分析数据


def gensentiments_snownlp(df):
    comments = df

    comments['sentiments'] = comments['cdescription'].apply(
        lambda x: SnowNLP(x).sentiments)

    # comments.to_csv('comm.csv')
    return comments


# __main__


if __name__ == '__main__':

    skus = read_skuinfo()
    newskus = nomalize_skus(skus)
    updateskus(newskus)

    comments = read_comments()
    comments2 = nomalize_comments(comments)
    comments3 = gensentiments_snownlp(comments2)
    updatecomments(comments3)
