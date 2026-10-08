from datetime import datetime
import smbus

class PicComms:

    def __init__(self, fixture=None):
        self.bus = fixture or smbus.SMBus(11)  # pylint: disable=I1101

    @property
    def date(self):
        return self.bus.get_date()
