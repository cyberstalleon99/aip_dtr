from datetime import datetime

def validate(date_str):
    date_format = "%Y-%m-%d"
    try:
        datetime.strptime(date_str, date_format)
    except ValueError:
        return False
    else:
        return True