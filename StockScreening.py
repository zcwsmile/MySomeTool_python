#coding:gbk
import urllib
import urllib2
import  cookielib
import json
import re
import random
import datetime
today = datetime.datetime.today()
yestoday = today - datetime.timedelta(days = 1)
tomorrow = today + datetime.timedelta(days = 1)
yesrq = yestoday.strftime('%Y%m%d')
todrq = today.strftime('%Y%m%d')
import os
def gupiao():
    l = ["ƽ������(000001)", " ���A(000002)", " PT����A(000003)", " ��ũ�Ƽ�(000004)", " ������Դ(000005)", " ����ҵA(000006)"]
    try:
        f1 = open('%s'%yesrq,'r')
        content = f1.readlines()
        f1.close()
    except:
        f1 = open('%s'%yesrq,'w')
        content = []
        f1.close()
    f = open('%s'%todrq,'w')
    f3 = open('ɸѡ���%s'%todrq,'w')
    for line in l:
        url = "http://hq.sinajs.cn/list=sz%s"%(line.split('(')[1].split(')')[0])
        resp = urllib2.urlopen(url)
        xh = resp.read()
        gpdm,sz = xh.split('=')
        sz = sz.split(';')[0].strip('"').replace(',','|')
        if sz == "":
            continue
        tmp = sz.split('|')
        print tmp[3],tmp[5]
        for i in content:
            if gpdm in i:
                temp = i.split('|')
                print temp
                print tmp[3] ,temp[6],int(tmp[8]),int(temp[11])
                if tmp[3] >= temp[6] and int(tmp[8])*10<=int(temp[11])*9:
                    f3.write(gpdm+'|'+sz+'\n')
                content.remove(i)
        f.write(gpdm+'|'+sz+'\n')
    f.close()
    f3.close()
    return xh
print gupiao()
