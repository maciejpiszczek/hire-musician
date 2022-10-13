from math import floor


def calculate_timedelta(curr_dt, last_update):
    tdelta = curr_dt - last_update
    if 1 < tdelta.seconds / 86400:
        td = str(floor(tdelta.seconds / 86400)) + ' days'
    elif 1 < tdelta.seconds / 3600 < 24:
        td = str(floor(tdelta.seconds / 3600)) + ' hours'
    elif 2 < tdelta.seconds / 60 < 60:
        td = str(floor(tdelta.seconds / 60)) + ' minutes'
    elif 1 < tdelta.seconds / 60 < 2:
        td = str(floor(tdelta.seconds / 60)) + ' minute'
    elif tdelta.seconds / 60 < 1:
        td = 'less than a minute'
    return td
