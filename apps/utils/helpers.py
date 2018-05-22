from calendar import monthcalendar, monthrange
from datetime import date, datetime, timedelta


def after_last_scrape(test_date, cutoff_date):
    '''
    Takes two date strings, converts them into datetime.date objects
    returns True if date1 is more recent than date2
    '''
    new_date = datetime.strptime(str(test_date), '%m/%d/%Y')
    cut_date = datetime.strptime(str(cutoff_date), '%m/%d/%Y')
    if new_date > cut_date:
        print (f"{test_date} is after {cutoff_date}")
    else:
        print (f"{test_date} is before {cutoff_date}")
    return new_date > cut_date

def before_cutoff_date(test_date, cutoff_date):
    '''Returns true if date1 is before date2, false otherwise'''
    new_date = datetime.strptime(str(test_date), '%m/%d/%Y')
    cut_date = datetime.strptime(str(cutoff_date), '%m/%d/%Y')

    return new_date < cut_date


def dateField_format(dater):
    '''converts datestring to YYYY-MM-DD format expected by datefield'''
    return datetime.strptime(dater, '%m/%d/%Y').strftime('%Y-%m-%d')

def formatted_date(dater):
    return dater.strftime('%m/%d/%Y')

def last_scrape_date():
    td = last_sunday()
    td -= timedelta(days=6)
    return td

def last_sunday():
    d = date.today()
    if d.weekday() is 6:
        return d
    while d.weekday() is not 6:
        d -= timedelta(days=1)
    return d

def list_blend(list1, list2):
    '''when table scrape broken into odds and evens classes
    blends the odds and evens into one list'''
    # list 1 is always equal or greater than length of list2
    if len(list2) > len(list1):
        list1, list2 = list2, list1

    new_list = []
    x = 0
    while list1 or list2:

        # therefore if it's list 2s turn and it doesn't exist we don't get an error
        if x % 2 != 0 and list2:
            new_list.append(list2.pop(0))
        else:
            new_list.append(list1.pop(0))
        x += 1
    return new_list

def last_last_sunday():
    """
    Find and return the date of last sunday of this month, if it 
    hasn't happened yet, return the last sunday date of last month

    Use calendar, timedelta, and date libraries
    """
    today = date.today()
    year, month, = today.year, today.month 
    # if we aren't in the last week of the month, use last month
    if monthrange(year, month)[1] - 6 > today.day:
        if today.month == 1:
            # if its jan set month to 12 and the year by 1
            year, month = today.year - 1, 12
        else:
            month = month - 1
    last_sunday = months_last_sunday(month, year)
    print(datetime.strptime(f"{month}/{last_sunday}/{year}",
                            "%m/%d/%Y"))
    return datetime.strptime(f"{month}/{last_sunday}/{year}",
                            "%m/%d/%Y")




def months_last_sunday(month, year):
    """ 
    Takes a number 1 - 12 to represent the month and returns
    the date of the final sunday in that month
    """
    weeks = monthcalendar(year, month)
    weeks.reverse()
    for week in weeks:
        if week[-1] != 0:
            return week[-1]

def next_sunday():
    ''' increment one day until reaching the first Sunday in the future '''
    d = date.today() + timedelta(days=1)
    while d.weekday() is not 6:
        d += timedelta(days=1)
    return d

def none_project(project):
    for value in project.values():
        if value is None:
            print(f"VALUE:{value} is equal to None")
            return True
    return False
