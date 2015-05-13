#!/usr/bin/env python
#coding:utf-8
"""
   Author: Kiveen
  Purpose: 某一天的1min修复对应日线数据
  Created: 2015/05/04
"""

import os
import os.path
import glob
import time
import struct
import re


def  StatisticsKline():
        """遍历数据为生成日k线oneKline"""
        global oneKline
        if oneKline[1] < 0.01:
                oneKline[1] = tupKline[1]        
        oneKline[2] = tupKline[2]
        if oneKline[3] < tupKline[3]:
                oneKline[3] = tupKline[3]
        if oneKline[4] > tupKline[4] or oneKline[4] < 0.01:
                oneKline[4] = tupKline[4]
        #print oneKline

 
def  RepairDayFile():
        newTempFileDir = "%s-1" % (repairFileDir)
        fileRe = open(repairFileDir,"rb")
        newfileWr = open(newTempFileDir,"wb")
        
        bIsAdd = 1          # 1 还未修改
        lastDayPri = 0      #昨收   直接上一条收盘就当昨收

        try:
                while True:                     
                        rdata = fileRe.read(36)
                        if not rdata:
                                break
                        tupKline = struct.unpack("Ifffffqf", rdata)
                        #print tupKline
                        strtim = time.localtime(tupKline[0])
                        if strtim.tm_yday >= nyDay and bIsAdd:
                                if strtim.tm_yday > nyDay:                 
                                        writeNewData=struct.pack('Ifffffqf',timKline,oneKline[1],oneKline[2],oneKline[3],oneKline[4],0,0,lastDayPri)
                                        newfileWr.write(writeNewData)
                                        bIsAdd = 0
                                        print "add this kdata"
                                else:
                                        print tupKline
                                        newDaykdata = list(tupKline)
                                        newDaykdata[1:5] = oneKline[1:5]
                                        tupKline = tuple(newDaykdata)
                                        bIsAdd = 0
                                        print newDaykdata
                        writeData=struct.pack('Ifffffqf',tupKline[0],tupKline[1],tupKline[2],tupKline[3],tupKline[4],tupKline[5],tupKline[6],lastDayPri)      
                        newfileWr.write(writeData)
                        lastDayPri = tupKline[2]
                if strtim.tm_yday < nyDay and bIsAdd:
                        if oneKline[7] < 0.01:
                                print "1min统计该天昨收值为0，请手动修改该日线昨收"                                      
                        writeNewData=struct.pack('Ifffffqf',timKline,oneKline[1],oneKline[2],oneKline[3],oneKline[4],0,0,oneKline[7])
                        newfileWr.write(writeNewData)
                        bIsAdd = 0
                        print "add end this kdata"
                        
        finally:
                fileRe.close()
                newfileWr.close()
                os.remove(repairFileDir)
                os.rename(newTempFileDir, repairFileDir)


if __name__=='__main__':
        dictDayKline = {}   #存放自己统计出来的天日线数据
        rootdir = os.getcwd()

        for folderdir in glob.glob(rootdir + os.sep + 'KLine*'):
                print folderdir, '--------------------------------'
                matched = re.search('([0-9]{4}_[0-9]{2}_[0-9]{2}$)', folderdir)
                if matched is None:
                        continue

                timFolder = time.strptime(matched.group(), "%Y_%m_%d")
                timKline = int(time.mktime(timFolder))
                nyDay = timFolder.tm_yday
                
                for file1min in os.listdir(folderdir):
                        fileProduct = os.path.basename(file1min).split('-')[0]
                        #print file1min, fileProduct
                        readFileDir1min = folderdir + os.sep + file1min
                        print readFileDir1min 
                        file_object = open(readFileDir1min, 'rb')
                        try:
                                rdata = file_object.read(32)
                                if not rdata:
                                        print readFileDir1min, ", data is less 32b."
                                oneKline = list(struct.unpack("IfffffIf", rdata))
                                #print oneKline
                                while True:
                                        rdata = file_object.read(32)
                                        if not rdata:
                                                break
                                        tupKline = struct.unpack("IfffffIf", rdata)
                                        #print tupKline 
                                        StatisticsKline()
                        finally:
                                file_object.close()
                        repairFileDir = "%s\\Kline%d\\%s-5.kline" % (rootdir, timFolder.tm_year, fileProduct)
                        print repairFileDir
                        print oneKline 
                        RepairDayFile()
                        oneKline = []
                timFolder = 0
                
        raw_input("Done, please input Enter to close ...")




