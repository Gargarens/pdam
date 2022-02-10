import datetime


def timeDeltaToMinSec(timedelta: str):
    clean = timedelta.split(".")
    parts = clean[0].split(":")
    minutes = parts[1]
    seconds = parts[2]
    return minutes + "min " + seconds + "sec"