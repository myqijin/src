#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql import DatabaseError


class Mysql():

    def __init__(self, host, port, user, password, db, charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.connsql = None
        self.cursor = None

    def connect(self):
        try:
            # establish database connection
            self.connsql = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                           db=self.db,
                                           charset=self.charset)
            # obtain cursor
            self.cursor = self.connsql.cursor()
        except DatabaseError as e:
            print(e)
        else:
            print("Connected Successfully")
            print(self.connsql)

    def dbclose(self):
        """close cursor"""
        self.cursor.close()
        self.connsql.close()
        print("db closed")

    def select(self, select):
        """SQL select"""
        # execute sql command
        self.cursor.execute(select)
        results = self.cursor.fetchall()
        return results

    def insert(self, insert):
        """insert one piece of data"""

        try:
            # execute sql command
            effect_row = self.cursor.execute(insert)
            print(self.cursor.rowcount)
            # raise command to database
            self.connsql.commit()
        except Exception as e:
            print(e)
            # if error exsits, database will be rollback
            self.connsql.rollback()
        else:
            return effect_row

    def execute(self, query):
        """execute one """
        try:
            # execute sql command
            effect_row = self.cursor.execute(query)
            # raise command to database
            self.connsql.commit()
        except Exception as e:
            print(e)
            # if error exsits, database will be rollback
            self.connsql.rollback()
        else:
            return effect_row
