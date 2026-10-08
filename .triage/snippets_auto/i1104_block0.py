import pytz


def example(datetime_obj):
    return pytz.UTC.localize(datetime_obj)
