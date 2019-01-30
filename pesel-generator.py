# -*- coding: utf-8 -*-

import datetime
import random
import time


def generate_pesel(from_date=None, to_date=None, gender=None):
    """
        from_date - start date in YYYY-MM-DD in format
        to_date - end date in YYYY-MM-DD in format
        gender - M for mem, F for women
    """

    if from_date is None:
        from_date = datetime.datetime(1800,1,1)
    else:
        from_date = datetime.datetime(int(from_date[0:4]), int(from_date[5:7]), int(from_date[8:10]))

    if to_date is None:
        to_date = datetime.datetime(2299, 12, 31)
    else:
        to_date = datetime.datetime(int(to_date[0:4]), int(to_date[5:7]), int(to_date[8:10]))

    if from_date.year<1800 or to_date.year>2299:
        raise Exception("Dates out of range")

    delta = to_date - from_date
    rand = random.random()
    rndDate = from_date + datetime.timedelta(days=rand * delta.days)

    yearPesel = rndDate.year % 100

    # shift months depend on year range
    monthPesel = rndDate.month
    if 1800 <= rndDate.year <= 1899:
        monthPesel += 80
    if 2000 <= rndDate.year <= 2099:
        monthPesel += 20
    if 2100 <= rndDate.year <= 2199:
        monthPesel += 40
    if 2200 <= rndDate.year <= 2299:
        monthPesel += 60

    dayPesel = rndDate.day

    rndValue = str(random.randint(1000,9999))
    # generate digit for gender
    if gender=='F':
        r = random.randrange(0, 10, 2)
        rndValue = str(random.randint(100,999)) + str(r)
    if gender=='M':
        r = random.randrange(1, 11, 2)
        rndValue = str(random.randint(100,999)) + str(r)

    pesel = "{:02d}{:02d}{:02d}{:4}".format(yearPesel, monthPesel, dayPesel, rndValue)

    # generate checksum
    check = 1*int(pesel[0]) + 3*int(pesel[1]) + 7*int(pesel[2]) + 9*int(pesel[3]) + 1*int(pesel[4]) + 3*int(pesel[5]) + 7*int(pesel[6]) + 9*int(pesel[7]) + 1*int(pesel[8]) + 3*int(pesel[9]) 
    if check % 10 == 0:
	    last_digit = 0
    else:
        last_digit = 10 - (check % 10)
    
    pesel = "{:9}{:01d}".format(pesel, last_digit)

    return pesel

###############################################################
# generate in loop
for x in range(10):
    pesel=generate_pesel("1980-01-01", "2019-12-31", gender='F')
    print(pesel)

for x in range(10):
    pesel=generate_pesel("1980-01-01", "2019-12-31", gender='M')
    print(pesel)
