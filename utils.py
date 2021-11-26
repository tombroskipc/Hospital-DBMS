import datetime
datetime.datetime.now()
import random
def get_year():
    return int(datetime.date.today().strftime('%Y'))

def get_today():
    return datetime.date.today().strftime('%Y-%m-%d')

def get_7_days_ago():
    return datetime.date.today() - datetime.timedelta(days=7)

def get_today_web_choice():
    return datetime.date.today().strftime('%m-%d-%Y')

# generate random number with 9 digits
def get_random_re_id():
    return random.randint(10000000, 99999999)

# def calculate_today_bill():
print(get_7_days_ago())