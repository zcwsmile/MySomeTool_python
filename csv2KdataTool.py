#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import os.path
import glob
import csv
import time
import struct
import string

dictProduct = {"XAUUSD":"3289648", "XAGUSD":"3355184", "AUDJPY":"3158321", "AUDNZD":"3682609", "AUDUSD":"3485745",
               "CADJPY":"3289393",  "CLWTI":"4534320", "EURAUD":"3486001", "EURCHF":"3420465", "EURGBP":"3354929",
               "EURJPY":"3682353", "EURUSD":"3223601", "GBPAUD":"3617073", "GBPCHF":"3551537", "GBPJPY":"3747889",
               "GBPUSD":"3354673", "NZDJPY":"3223857", "NZDUSD":"3551281", "USDCAD":"3616817", "USDCHF":"3420209",
               "USDJPY":"3289137",   "USDX":"3159344", "XBTUSD":"3158072", "USDCNH":"3748145", "HKDCNH":"3158577"}

dictShotProd = {"XAUUSD":"022", "XAGUSD":"023", "AUDJPY":"110", "AUDNZD":"118", "AUDUSD":"105",
               "CADJPY":"112", "CLWTI":"00E", "EURAUD":"115", "EURCHF":"114", "EURGBP":"113",
               "EURJPY":"108", "EURUSD":"101", "GBPAUD":"117", "GBPCHF":"116", "GBPJPY":"109",
               "GBPUSD":"103", "NZDUSD":"106", "USDCAD":"107", "USDCHF":"104", "USDX":"050",
               "USDJPY":"102", "NZDJPY":"111", "USDCNH":"119", "HKDCNH":"120"}

dictType = {'M1':35, 'M5':1, 'Daily':5, 'Weekly':6, 'Monthly':7}  # M15 M30 H1 H4}

def funCreatefile(linedata):
    """
     生成文件.kline:
    """
    strtim = time.strptime(linedata[0], "%Y.%m.%d %H:%M")
    
    tim = int(time.mktime(strtim))
    starPri = string.atof(linedata[1])
    endPri = string.atof(linedata[4])
    highPri = string.atof(linedata[2])
    lowPri = string.atof(linedata[3])

    if starPri<0.1 or endPri<0.1 or highPri<0.1 or lowPri<0.1:
        print "haveErr:price too litter", linedata 
        return

    global g_year
    global g_yday
    global fyestDayPri
    global fpKdata 


    if fileType == 'Daily':
        if strtim.tm_year != g_year:
            fileDir = "KLine%04d" % (strtim.tm_year)
            print "./",fileDir,"/", fileName
            if strtim.tm_year != (g_year+1):
                fyestDayPri = 0
            g_year = strtim.tm_year
            if fpKdata != 0:
                fpKdata.close()
                os.chdir('../')
            if not os.path.exists(fileDir):
                os.mkdir(fileDir)
            os.chdir(fileDir)
            fpKdata = open(fileName,'wb')


    elif fileType in 'WeeklyMonthly':
            fileDir = "KLineWeekMonth"
            print "./",fileDir,"/", fileName
            # if fpKdata != 0:
            #     fpKdata.close()
            #     os.chdir('../') 
            if fpKdata == 0:
                if not os.path.exists(fileDir):
                    os.mkdir(fileDir)
                os.chdir(fileDir)
                fpKdata = open(fileName,'wb')


    elif fileType in 'M1M5':
        if strtim.tm_hour >= 22:
            strtim = time.localtime(tim + 3600*24)

        if strtim.tm_yday != g_yday:
            fileDir = "KLine%04d_%02d_%02d" % (strtim.tm_year, strtim.tm_mon, strtim.tm_mday)
            print "./",fileDir,"/", fileName

            if strtim.tm_yday != (g_yday+1):
                fyestDayPri = 0
            g_yday = strtim.tm_yday
            if fpKdata != 0:
                fpKdata.close()
                os.chdir('../')
            if not os.path.exists(fileDir):
                os.mkdir(fileDir)
            os.chdir(fileDir)
            fpKdata = open(fileName,'wb')
        
    #Dalist = [tim, starPri, endPri, highPri, lowPri, 0, 0, fyestDayPri]
    if fileType == 'M1':
        writeData = struct.pack('IfffffIf',tim, starPri, endPri, highPri, lowPri, 0, 0, fyestDayPri)
    elif fileType in 'DailyWeeklyMonthly':
        writeData = struct.pack('Ifffffqf',tim, starPri, endPri, highPri, lowPri, 0, 0, fyestDayPri)
    elif fileType == 'M5':
        writeData = struct.pack('IfffffI',tim, starPri, endPri, highPri, lowPri, 0, 0)

    fyestDayPri = endPri

    fpKdata.write(writeData)


def funReadcsv():
    """
    读csv
    """
    pcsvf = file(filecsv, 'rb')
    reader = csv.reader(pcsvf)
    for linedata in reader:
        funCreatefile(linedata)
    pcsvf.close()


if __name__=='__main__':
    #os.chdir('../')           #转成exe时需要用

    rootdir = os.getcwd()                 # 指明被遍历的文件夹
    numHandleFile = 0
    numErrorFile = 0
        
    for filecsv in glob.glob(rootdir + os.sep + '*.csv'):    #遍历当前文件夹内目标文件
        os.chdir(rootdir)
        #print os.getcwd()
        fyestDayPri = 0
        g_year = 0
        g_yday = 0
        fpKdata = 0

        if os.path.isdir(filecsv):
            continue
        else:
            fileProduct = os.path.basename(filecsv).split(' ')[0]       #产品名
            if fileProduct not in dictShotProd :
                print "one Error:", filecsv, "Product not in dictShotProd"
                numErrorFile = numErrorFile + 1
                continue
            fileType = os.path.basename(filecsv).split(' ')[1].split('.')[0]
            if fileType not in dictType :
                print "one Error: no identify dictType", filecsv, "Type not in dictType:", dictType.keys()
                numErrorFile = numErrorFile + 1
                continue            
            print filecsv, fileProduct, fileType
            fileName = "%s-%d.kline" % (dictShotProd[fileProduct], dictType[fileType])
            numHandleFile = numHandleFile + 1
            funReadcsv()

        if fpKdata != 0:
            fpKdata.close()
            fpKdata = 0
    print "numHandleFile:", numHandleFile, ";  numErrorFile:", numErrorFile
    raw_input("Done, please input Enter to close ...")





