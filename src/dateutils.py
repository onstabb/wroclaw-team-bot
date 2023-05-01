from datetime import datetime, timedelta

import pytz

from src.config import MAIN_TIMEZONE


def get_now() -> datetime:
    """ Get the timezone-awareness datetime """
    return datetime.now(pytz.utc)


def get_now_main_tz() -> datetime:
    return datetime.now(MAIN_TIMEZONE)


def get_next_week_monday(date: datetime) -> datetime:
    return date + timedelta(days=(7 - date.weekday()))


def get_week_range(date: datetime) -> tuple[datetime, datetime]:
    start_of_week: datetime = date - timedelta(days=date.weekday())
    end_of_week: datetime = start_of_week + timedelta(days=6)

    return start_of_week.replace(hour=0, minute=0, second=0, microsecond=0), \
           end_of_week.replace(hour=23, minute=59, second=59, microsecond=9)


def is_in_current_week(date: datetime.date) -> bool:
    start_of_week, end_of_week = get_week_range(date)
    if end_of_week >= date >= start_of_week:
        return True
    return False


def get_weeks_delta(start_date: datetime, end_date: datetime) -> int:
    monday_1: datetime = (start_date - timedelta(days=start_date.weekday()))
    monday_2: datetime = (end_date - timedelta(days=end_date.weekday()))

    return (monday_2 - monday_1).days // 7


if __name__ == '__main__':
    pass
