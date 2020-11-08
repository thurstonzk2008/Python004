#!/usr/bin/python3
# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup as bs
import random
import time
import pymysql


def get_movieinfo(url):
    """爬取电影短评相关信息：肖申克的救赎
    """

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'Referer': 'https://movie.douban.com/subject/1292052/'
        }

        response = requests.get(url, headers=headers)
        bs_info = bs(response.text, 'html.parser')

        # 汇总电影短评信息
        for movie_data in bs_info.find_all('div', attrs={"class": "comment-item"}):
            short_comments = movie_data.find(
                'span', attrs={"class": "short"}).get_text().strip()
            comment_time = movie_data.find(
                'span', attrs={"class": "comment-time"}).get_text().strip()
            star_rating = str(movie_data.find(
                'span', attrs={"class": "rating"}))

            if 'allstar50' in star_rating:
                star_num = 5
            elif 'allstar40' in star_rating:
                star_num = 4
            elif 'allstar30' in star_rating:
                star_num = 3
            elif 'allstar20' in star_rating:
                star_num = 2
            elif 'allstar10' in star_rating:
                star_num = 1
            else:
                star_num = 0

            movie_info.append((short_comments, star_num, comment_time))

    except Exception as e:
        print(e)


class StoreDB(object):
    """将获取的内容存入数据库中

    执行批量插入
    """

    def __init__(self, dbInfo, movie_info):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']
        self.table = dbInfo['table']
        self.movie_info = movie_info

    def run(self):
        try:
            pymysql_connect = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db
            )
            connect_cursor = pymysql_connect.cursor()

            # 执行批量插入
            connect_cursor.executemany(
                f'INSERT INTO {self.table} (short_comments, star_num, comment_time) values(%s, %s, %s)', self.movie_info)
            pymysql_connect.commit()

            connect_cursor.close()
        except:
            pymysql_connect.rollback()
        finally:
            pymysql_connect.close()


movie_info = []  # 电影短评相关信息汇总


if __name__ == "__main__":
    # 获取前 5 页短评内容：共 100 条
    urls = tuple(
        f'https://movie.douban.com/subject/1292052/comments?start={20 * page}&limit=20&status=P&sort=new_score' for page in range(5))
    for url in urls:
        get_movieinfo(url)
        time.sleep(random.uniform(2, 6))

    # 将获取的内容存入数据库中
    dbInfo = {
        'host': '192.168.3.100',
        'port': 3306,
        'user': 'root',
        'password': 'Password123',
        'db': 'db_week',
        'table': 'tb_douban'
    }
    db = StoreDB(dbInfo, movie_info)
    db.run()
