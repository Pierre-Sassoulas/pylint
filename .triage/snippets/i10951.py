from enum import IntEnum


class LogLevel(IntEnum):
    from syslog import LOG_CRIT as CRITICAL
    from syslog import LOG_DEBUG as DEBUG
    from syslog import LOG_EMERG as EMERGENCY
    from syslog import LOG_ERR as ERROR
    from syslog import LOG_INFO as INFO
    from syslog import LOG_WARNING as WARNING


print(LogLevel.EMERGENCY.value)
