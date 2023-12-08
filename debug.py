from datetime import datetime as dt


FILENAME = 'debug.txt'


def log(info, level='DEBUG'):
    time_str = str(dt.now()).split('.')[0]
    open(FILENAME, 'a').write(f"\n{time_str} | {info} | [{level}]")

