#!/usr/bin/python
#-*- coding: utf-8 -*-

import time
import datetime
from datetime import timedelta

def calc_fat_thursday(year):
    a = year%19
    b = int(year/100)
    c = year%100
    d = int(b/4)
    e = b%4
    f = int((b+8)/25)
    g = int((b-f+1)/3)
    h = (19*a+b-d-g+15)%30
    i = int(c/4)
    k = c%4
    l = (32+2*e+2*i-h-k)%7
    m = int((a+11*h+22*l)/451)
    p = (h+l-7*m+114)%31
    day = p+1
    month = int(h+l-7*m+114)/31

    dt = datetime.datetime(year, month, day) - timedelta(days=52)

    return (dt.year, dt.day, dt.month)


for year in range(2019, 2039):    
    (y,d,m)=calc_fat_thursday(year)
    print "Fat Thursday day in {:04d} - {:04d}-{:02d}-{:02d}".format(year, y, m, d )

