from datetime import date, datetime, timedelta
from random import randint

def short_date():
    ''' returns a date within 45 days of current date'''
    days=randint(0,45)
    new_date = date.today() + timedelta(days=days)
    return new_date

def long_date():
    ''' returns a date outside of 45 days of current date'''
    days=randint(45,730)
    new_date = date.today() + timedelta(days=days)
    return new_date

def rand_date():
    var = randint(0,1)
    if var is 1:
        return long_date()
    else:
        return short_date()
        
