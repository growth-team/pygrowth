import arrow


def datetime_to_str(time):
    return str(arrow.get(time)).split("+")[0] + "Z"
