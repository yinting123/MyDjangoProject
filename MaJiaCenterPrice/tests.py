# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from views import *
# Create your tests here.

db = MysqlDB()
# db.findMajia(check_in='20170516',mhotel='50101002',mroom='1049',breakfast=1,payment=0)
# db.generateMajia(0,1)
# db.generateMajia(0,1,30101023,1049,100,200,1,0)
db.findMajia(1,30101023,1051,1,0)
# db.insertMajia(0,1,30101023,1051,100,200,1,0)
