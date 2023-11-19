from datetime import datetime

date_formats = [
    '%Y-%m-%d',
    '%Y/%m/%d',
    '%Y.%m.%d',
    '%Y-%m-%d',
    '%Y/%m/%d',
    '%Y.%m.%d',
    '%d-%m-%Y',
    '%d/%m/%Y',
    '%d.%m.%Y',
    '%m-%d-%Y',
    '%m/%d/%Y',
    '%m.%d.%Y',
    '%B %d, %Y',
    '%d %B %Y',
    '%b %d, %Y',
    '%d %b %Y',
    '%d %b, %Y',
    '%Y%m%d',
    '%d%m%Y'
    ]

def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    return new_phone

def to_timestamp(date):
    for format_str in date_formats:
        try:
            date_object = datetime.strptime(date, format_str)
            # return date_object.timestamp()
            return int(date_object.timestamp())
        except ValueError:
            pass
    return False