from enum import Enum
from typing import Protocol

class WeekDay(Enum):
    Monday = 'monday'

class Event(Protocol):
    def weekday(self) -> WeekDay: ...

class EventMix(Event):
    def do(self):
        print(f'weekday={self.weekday.value}')

class MyEvent(EventMix):
    def __init__(self) -> None:
        self.weekday = WeekDay.Monday

my_event = MyEvent()
my_event.do()
