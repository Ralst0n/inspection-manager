from datetime import date, datetime, timedelta


def after_last_scrape(test_date, cutoff_date):
    '''
    Takes two date strings, converts them into datetime.date objects
    returns True if date1 is more recent than date2
    '''
    new_date = datetime.strptime(str(test_date), '%m/%d/%Y')
    cut_date = datetime.strptime(str(cutoff_date), '%m/%d/%Y')
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

        #therefore if it's list 2s turn and it doesn't exist we don't get an error
        if x % 2 != 0 and list2:
            new_list.append(list2.pop(0))
        else:
            new_list.append(list1.pop(0))
        x += 1
    return new_list



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
