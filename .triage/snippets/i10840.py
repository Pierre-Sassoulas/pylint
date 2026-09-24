import os
from enum import StrEnum


class Env(StrEnum):
    LOG_LEVEL = "LOG_LEVEL"


os.getenv(Env.LOG_LEVEL, "INFO")
