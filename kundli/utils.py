
def convert_time(hour,offset):

    #hour = 15
    #offset = -6.5

    offset = float(offset)/3600

    hour += offset

    if hour < 0:
        hour += 24
    else:
        hour %= 24

    return hour

