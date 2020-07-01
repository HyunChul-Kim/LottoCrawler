from datetime import datetime


def gab_of_weeks(update):
    update_date_split = update.split('-')
    u_date = datetime(int(update_date_split[0]), int(update_date_split[1]), int(update_date_split[2]))
    c_date = datetime.now()
    gab = int((c_date - u_date).days / 7)
    return gab


def is_saturday():
    """
    0: Monday 1: Tuesday 2: Wednesday 3: Thursday 4: Friday 5: Saturday 6: Sunday
    """
    date = datetime.now()
    return date.weekday() == 5

