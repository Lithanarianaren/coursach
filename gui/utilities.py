from datetime import datetime


def check_date(d: int, m: int, y: int):
    def leap_year(year: int) -> bool:
        return year % 400 == 0 or (year % 100 != 0 and year % 4 == 0)

    months = [31, 29 if leap_year(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if not (1 <= d <= months[m]): return False
    if not (1 <= m <= 12): return False
    return True


def n_numbers(number, n):
    s = ''
    for i in range(n):
        s = str((number // (10 ** i)) % 10) + s
    return s


def dd_mm_yyyy(dd, mm, yyyy):
    return f"{n_numbers(dd, 2)}/{n_numbers(mm, 2)}/{n_numbers(yyyy, 4)}"


def get_datetime():
    now = datetime.now()
    return f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}"

def get_tuple_datetime():
    now = datetime.now()
    return now.day, now.month, now.year