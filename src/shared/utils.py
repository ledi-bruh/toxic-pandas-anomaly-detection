import datetime as dt


__all__ = ['now']


def now() -> dt.datetime:
    return dt.datetime.now(tz=dt.UTC)
