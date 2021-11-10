import datetime
datetime.datetime.now()

def get_year():
    return int(datetime.date.today().strftime('%Y'))

def get_today():
    return datetime.date.today().strftime('%Y-%m-%d')

def get_today_web_choice():
    return datetime.date.today().strftime('%m-%d-%Y')