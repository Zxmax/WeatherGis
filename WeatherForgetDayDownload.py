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
            s = s.replace(c, '')
    return s


def DateSQL(year, mon):
    if mon in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        return 'weather_' + str(year) + '_0' + str(mon)
    else:
        return 'weather_' + str(year) + '_' + str(mon)


def DateMon(year, mon):
    if mon in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        return str(year) + '年0' + str(mon) + '月天气'
    else:
        return str(year) + '年' + str(mon) + '月天气'


def DateComplete(year, mon, day):
    if mon in [1, 2, 3, 4, 5, 6, 7, 8, 9] and day in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        return str(year) + '-0' + str(mon) + '-0' + str(day)
    elif mon in [1, 2, 3, 4, 5, 6, 7, 8, 9] and day not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        return str(year) + '-0' + str(mon) + '-' + str(day)
    else:
        return str(year) + '-' + str(mon) + '-' + str(day)


def GetHisWeather(list, year, mon, day):
    url = "http://lishi.tianqi.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    for position_get in soup.select('.bcity li a'):
        if position_get.string in list_all:
            # print(position_get.string)
            position = position_get.text
            print(position+'done.')
            res2 = requests.get(position_get['href'])
            soup2 = BeautifulSoup(res2.text, 'html.parser')
            for WeatherHis_get in soup2.select('.tqtongji1 ul li a'):
                date_Mon = DateMon(year, mon)
                if WeatherHis_get.text == date_Mon:
                    res3 = requests.get(WeatherHis_get['href'])
                    soup3 = BeautifulSoup(res3.text, 'html.parser')
                    for DataItem in soup3.select('.tqtongji2 ul'):
                        flag = 0
                        weatherinfo = []
                        for item in DataItem.select('li'):
                            if item.string == DateComplete(year, mon, day) and flag == 0:
                                date = item.text
                                flag = 1
                            elif flag == 1:
                                weatherinfo.append(item.string)
                        if flag == 1:
                            #如果文件不存在，会自动在当前目录创建:
                            conn = sqlite3.connect('weatherinfo.db')
                            # 创建一个Cursor:
                            cursor = conn.cursor()
                            # 执行一条SQL语句，创建user表:
                            tableName = DateSQL(year, mon)
                            sql = 'create table ' + tableName + '(\
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
                                cursor.execute(
                                    'insert into ' + tableName + ' (position,date,Top_temp,Low_temp,weather,wind_direction,wind_power) values (\'' + position + '\', \'' + date + '\',\'' +
                                    weatherinfo[0] + '\',\'' + weatherinfo[1] + '\',\'' + weatherinfo[2] + '\',\'' +
                                    weatherinfo[3] + '\',\'' + weatherinfo[4] + '\')')
                                # 通过rowcount获得插入的行数:
                                # print(cursor.rowcount)
                                # 提交事务:
                                conn.commit()
                            except:
                                conn.rollback()
    print(date+'History Weather Download success')


list_hangzhou = ['萧山', '余杭', '富阳', '上城区', '下城区', '江干区', '拱墅区', '西湖区', '滨江区', '桐庐', '淳安', '建德', '临安']
list_huzhou = ['南浔', '吴兴区', '长兴', '安吉', '德清']
list_jiaxing = ['南湖区', '秀洲区', '嘉善', '海宁', '桐乡', '平湖', '海盐']
list_ningbo = ['北仑', '鄞州', '镇海', '海曙区', '江东区', '江北区(暂无)', '慈溪', '余姚', '奉化', '象山', '宁海']
list_shaoxing = ['上虞', '越城区', '柯桥区(暂用上虞)', '诸暨', '新昌', '嵊州']
list_taizhou = ['椒江', '黄岩', '路桥', '玉环', '三门', '天台', '仙居', '温岭', '临海', '洪家']
list_wenzhou = ['鹿城区', '龙湾区', '瓯海区', '洞头', '泰顺', '文成', '平阳', '永嘉', '苍南', '瑞安', '乐清']
list_lishui = ['莲都区', '古城区', '遂昌', '缙云', '青田', '云和', '庆元', '松阳', '景宁', '龙泉']
list_jinhua = ['婺城区', '金东区', '浦江', '武义', '磐安', '兰溪', '义乌', '东阳', '永康', '横店']
list_quzhou = ['柯城区', '衢江', '常山', '开化', '龙游', '江山']
list_zhoushan = ['普陀', '定海', '嵊泗', '岱山']
list_all = list_hangzhou + list_jiaxing + list_jinhua + list_lishui + list_ningbo + list_quzhou + list_shaoxing + list_taizhou + list_huzhou + list_wenzhou + list_zhoushan

GetHisWeather(list, 2018, 2, 1)
