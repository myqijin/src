#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql


class mysql():

    def __init__(self, host, port, user, password, db, charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        # establish database connection
        self.connsql = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                       db=self.db, charset=self.charset)
        # obtain cursor
        self.cursor = self.connsql.cursor()

    def dbclose(self):
        self.cursor.close()
        self.connsql.close()

    def select(self, tablename, fields, conts):

        # SQL select
        select = "select * from" + tablename + " where " + fields + " is " + conts
        try:
            # execute sql command
            self.cursor.execute(select)
            results = self.cursor.fetchall()
        except Exception as e:
            print("No Found!")
        return results

    def insert(self, tablename, fields, conts):

        # SQL insert
        results = self.select(tablename, fields, conts)

        # if
        if results == None:
            insert = "INSERT INTO " + tablename + " (" + fields + ") values (" + conts + ")"
            try:
                # execute sql command
                self.cursor.execute(insert)
                print(self.cursor.rowcount)
                # raise command to database
                self.connsql.commit()
            except Exception as e:
                print(e)
                # if error exsits, database will be rollback
                self.connsql.rollback()
