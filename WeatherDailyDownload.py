#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import time
import sqlite3
from bs4 import BeautifulSoup

def OnlyNum(s):
    fomart = '0123456789~℃'
    for c in s:
        if not c in fomart:
            s = s.replace(c,'')
    return s

def DateFormat(date):
    date=date.replace('年','-')
    date=date.replace('月','-')
    date=date.replace('日','')
    return date

def getDailyWeather(position,date,Top_temp,Low_temp,weather,wind_direction,wind_power):
    url="http://www.tianqi.com/province/zhejiang/"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    for position_get in soup.select(".racitys li span a"):
        position=position_get.text
        url2='http://www.tianqi.com'+position_get['href']
        res2=requests.get(url2)
        soup2=BeautifulSoup(res2.text,'html.parser')
        j=1
        for tempinfo in soup2.select(".weather_info dd"):
            if j==2:
                date=tempinfo.text[0:12]
            if j==3:
                s = OnlyNum(tempinfo.text)
                flag3=s.find('℃')
                flag4=s.rfind('℃')
                flag5=s.find('~')
                Low_temp=s[flag3+1:flag5]
                Top_temp=s[flag5+1:flag4]
            j=j+1
        i=1
        for weatherinfo in soup2.select(".weather_info dd b"):
            if i==2:
                weather=weatherinfo.text
            if i==4:
                windinfo=weatherinfo.text
                flag1=windinfo.index('：')
                flag2=windinfo.index(' ')
                wind_direction=windinfo[flag1+1:flag2]
                wind_power=windinfo[flag2+1:]
            i=i+1
        #print(position, date, Top_temp, Low_temp, weather, wind_power, wind_direction)
        time.sleep(0.5)
        tableName = date.replace('年', '_')
        tableName = 'weather_' + tableName[:tableName.index('月')]
        #print(tableName)
        date = DateFormat(date)
        # 如果文件不存在，会自动在当前目录创建:
        conn = sqlite3.connect('weatherinfo.db')
        # 创建一个Cursor:
        cursor = conn.cursor()
        # 执行一条SQL语句，创建user表:
        sql = 'create table '+tableName+'(\
            position VARCHAR(40) NOT NULL,\
            date VARCHAR(40) NOT NULL,\
            Top_temp VARCHAR(40) ,\
            Low_temp VARCHAR(40) ,\
            weather VARCHAR(40) ,\
            wind_direction VARCHAR(40) ,\
            wind_power VARCHAR(40), \
            PRIMARY KEY (position,date)\
            );'
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            conn.commit()
        except:
            # 如果发生错误则回滚
            conn.rollback()
        try:
            # 继续执行一条SQL语句，插入一条记录:
            cursor.execute('insert into '+tableName+' (position,date,Top_temp,Low_temp,weather,wind_direction,wind_power\
                            ) values (\''+position+'\', \''+date+'\',\''+Top_temp+'\',\''+Low_temp+'\',\''+weather+'\',\''+wind_direction+'\',\''+wind_power+'\')')
            # 通过rowcount获得插入的行数:
            #print(cursor.rowcount)
            # 提交事务:
            conn.commit()
        except:
            conn.rollback()

position=""
date=""
Top_temp=""
Low_temp=""
weather=""
wind_direction=""
wind_power=""
getDailyWeather(position,date,Top_temp,Low_temp,weather,wind_direction,wind_power)
print(date+'Download successful')
