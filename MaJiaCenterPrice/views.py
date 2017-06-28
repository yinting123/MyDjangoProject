# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from conf import *
from datetime import datetime,timedelta
import MySQLdb
import ConfigParser


# Create your views here.

def majia(request):
    return render(request,'majiaInput.html')

def sucess(request):
    return render(request,'ShowResult.html')

def error(request):
    return render(request,'error.html')

def insertMajia(request):
    sucess = True
    if request.method == "POST":
        ci = int(request.POST.get('check_in'))
        co = int(request.POST.get('check_out'))
        mhotel = int(request.POST.get('elong_mhotel'))
        mroom = int(request.POST.get('elong_mroom'))
        pay = int(request.POST.get('settlement'))
        breakfast = int(request.POST.get('breakfast'))
        cprice = int(request.POST.get('ctrip_price'))
        qprice = int(request.POST.get('qunar_price'))
        db = MysqlDB()
        sucess = db.insertMajia(ci,co,mhotel,mroom,cprice,qprice,pay,breakfast)
    if sucess:
        return render(request,'ShowResult.html')
    else:
        return render(request,'error.html')

def centerPrice(request):
    return render(request,"center-price.html")

def insertCenterPrice(request):
    sucess = True
    if request.method == "POST":
        ci = int(request.POST.get('check_in'))
        co = int(request.POST.get('check_out'))
        mhotel = int(request.POST.get('elong_mhotel'))
        mroom = int(request.POST.get('elong_mroom'))
        pay = int(request.POST.get('pay-type'))
        breakfast = int(request.POST.get('breakfast'))
        pc_price = int(request.POST.get('pc_deal_price'))
        app_price = int(request.POST.get('app_deal_price'))
        db = MysqlDB()
        sucess = db.insertCenterPrice(ci,co,mhotel,mroom,pay,breakfast,pc_price,app_price)
    if sucess:
        return render(request,'ShowResult.html')
    else:
        return render(request,'error.html')

class MysqlDB():
    def __init__(self):
        self.majia_type = ['mj_app_price', 'mj_pc_price']
        cfg = ConfigParser.ConfigParser()
        cfg.read('./conf/dataBase.conf')
        self.host = cfg.get('majia','host')
        self.port = cfg.getint('majia','port')
        self.user = cfg.get('majia','user')
        self.pwd = cfg.get('majia','pwd')
        self.name = cfg.get('majia','name')
        # print self.host,self.port,self.user,self.pwd,self.name

    def connect(self):
        try:
            conn = MySQLdb.connect(host=self.host,port = self.port,
                                   user = self.user,passwd=self.pwd,
                                   db=self.name)
        except Exception,e:
            print e
            print '连接马甲数据库失败'
        finally:
            print conn
            if conn is not None:
                return conn,conn.cursor()
            else:
                return conn,conn

    def findMajia(self,check_in,mhotel,mroom,payment,breakfast,type):
        """如果有相同的则删除 type 1:马甲 2：中央定价"""
        conn,cursor = self.connect()
        if type == 1:
            where = 'where elong_mhotel_id = %s and elong_mroom_id = %s ' \
                    'and pay_type = %s and breakfast_digit = %s' % \
                    (mhotel, mroom, payment, breakfast)
            for t in self.majia_type:
                sql = 'select * from %s_%s %s' \
                      % (t,self.timeStrf(self.DateTransfer(check_in),0),where)
                find = cursor.execute(sql)
                if find > 0:
                    delSql = 'delete from %s_%s %s' %(t,self.timeStrf(self.DateTransfer(check_in),0),where)
                    cursor.execute(delSql)
                    conn.commit()
        if type == 2:
            where = 'where checkin_date = %s and elong_mhotel_id = %s and ' \
                    'elong_mroom_id = %s and pay_type = %s and breakfast = %s'\
                    %(check_in,mhotel,mroom,payment,breakfast)
            sql = 'select * from center_price_%s %s' \
                  %(self.timeStrf(self.DateTransfer(check_in),0),where)
            find = cursor.execute(sql)
            if find:
                delSql = 'delete from center_price_%s %s' \
                         %(self.timeStrf(self.timeStrf(self.DateTransfer(check_in),0)),where)
                cursor.execute(delSql)
                conn.commit()
            pass
        cursor.close()
        conn.close()

    def generateMajia(self,ci,co,mhotel,mroom,cp,qp,pay,breakfast):
        sqls = []
        for i in xrange((co-ci+1)):
            self.findMajia(ci+i, mhotel, mroom, pay, breakfast,1)
            for type in self.majia_type:
                mj_tables = "%s_%s"%(type,self.timeStrf(self.DateTransfer(ci+i),0))
                baseSql = 'insert into %s ' \
                          '(checkin_date,elong_mhotel_id,elong_mroom_id,' \
                          'pay_type,breakfast_digit,ctrip_deal_price,' \
                          'qunar_deal_price,lowest_term,' \
                          'sync_date,update_date,qunar_mhotel_id)'\
                          'values(%s,%s,%s,%s,%s,%s,%s,1,now(),now(),11)'\
                          %(mj_tables,str(self.timeStrf(self.DateTransfer(ci+i),0)),\
                            mhotel,mroom,pay,breakfast,cp,qp)
                sqls.append(baseSql)
        return sqls

    def insertMajia(self,ci,co,mhotel,mroom,cp,qp,pay,breakfast):
        sqls = self.generateMajia(ci,co,mhotel,mroom,cp,qp,pay,breakfast)
        conn,cursor = self.connect()
        flag = True
        for sql in sqls:
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception,e:
                print e
                flag = False
                break
        cursor.close()
        conn.close()
        return flag


    def generateCenterPrice(self,check_in,check_out,mhotel,mroom,pay,
                            breakfast,pc_price,app_price):
        sqls = []
        for i in xrange((check_out-check_in+1)):
            self.findMajia(check_in,mhotel,mroom,pay,breakfast,2)
            ceter_tables = 'center_price_%s' %(self.timeStrf(self.DateTransfer(check_in+i),0))
            baseSql = 'insert into %s' \
                      '(checkin_date,elong_mhotel_id,elong_mroom_id,' \
                      'pay_type,breakfast,pc_deal_price,app_deal_price)' \
                      'values(%s,%s,%s,%s,%s,%s,%s)' \
                      %(ceter_tables,self.timeStrf(self.DateTransfer(check_in+i),0),\
                        mhotel,mroom,\
                        pay,breakfast,pc_price,app_price)
            # return
            sqls.append(baseSql)
        return sqls

    def insertCenterPrice(self,check_in,check_out,mhotel,mroom,pay,
                            breakfast,pc_price,app_price):
        sqls = self.generateCenterPrice(check_in,check_out,mhotel,mroom,pay,breakfast,pc_price,app_price)
        conn,cursor = self.connect()
        flag = True
        for sql in sqls:
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception,e:
                print e
                print '插入中央定价数据失败'
                flag = False
                break
        cursor.close()
        conn.close()
        return flag

    def DateTransfer(self, num):
        now = datetime.now()
        now += timedelta(num)
        return now

    def timeStrf(self, day, type):
        if type == 0:
            return datetime.strftime(day, "%Y%m%d")
        else:
            return datetime.strftime(day, "%Y-%m-%d")