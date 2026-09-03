from datetime import datetime


def format_date(date):

    if isinstance(date, str):
        date = datetime.fromisoformat(date)

    return date.strftime("%d %b %Y")