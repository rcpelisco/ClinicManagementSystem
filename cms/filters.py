from datetime import datetime
from dateutil.relativedelta import relativedelta

def format_datetime(value):
    datetime_object = value
    return datetime_object.strftime('%B %d, %Y - %I:%M %p')

def format_date(value):
    date_object = value
    return date_object.strftime('%B %d, %Y')

def format_age(value):
    dob = datetime.strptime(value, '%Y-%m-%d')
    today = datetime.today()
    age = relativedelta(today, dob)
    return age.years
