import datetime


class RtcDriver:
    def __init__(self, i2c_address):
        self._datetime = datetime.datetime.now()

    @property
    def datetime(self) -> datetime.datetime:
        return self._datetime

    @datetime.setter
    def datetime(self, date_time: datetime.datetime) -> None:
        self._datetime = date_time
