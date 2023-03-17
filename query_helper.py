import datetime

def get_month_dates(month):
    # Convert month name to month number (1-12)
    month_number = datetime.datetime.strptime(month, "%B").month

    # Get first day of the month
    start_date = datetime.date.today().replace(day=1, month=month_number)

    # Get last day of the month
    last_day = 31
    while True:
        try:
            end_date = start_date.replace(day=last_day)
            break
        except ValueError:
            last_day -= 1

    # Return start and end dates in YYYY-MM-DD format
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
