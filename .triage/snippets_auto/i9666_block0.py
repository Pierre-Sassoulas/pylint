"""Defines things required for the minimal example"""

from ctypes import POINTER, Structure
from ctypes.wintypes import DWORD
from enum import IntEnum

class SERVICE_STATUS(Structure):  # pylint: disable=invalid-name,too-few-public-methods
    """
    Service status structure.

    See:
     https://learn.microsoft.com/en-us/windows/win32/api/winsvc/ns-winsvc-service_status
    """

    _fields_ = [
        ("dwServiceType", DWORD),
        ("dwCurrentState", DWORD),
        ("dwControlsAccepted", DWORD),
        ("dwWin32ExitCode", DWORD),
        ("dwServiceSpecificExitCode", DWORD),
        ("dwCheckPoint", DWORD),
        ("dwWaitHint", DWORD),
    ]


LPSERVICE_STATUS = POINTER(SERVICE_STATUS)

class CurrentState(IntEnum):
    """Windows service manager service status codes"""

    SERVICE_CONTINUE_PENDING = 0x00000005
    SERVICE_PAUSE_PENDING = 0x00000006
    SERVICE_PAUSED = 0x00000007
    SERVICE_RUNNING = 0x00000004
    SERVICE_START_PENDING = 0x00000002
    SERVICE_STOP_PENDING = 0x00000003
    SERVICE_STOPPED = 0x00000001


class ControlsAccepted(IntEnum):
    """Windows service manager accepted service control codes"""

    SERVICE_ACCEPT_NETBINDCHANGE = 0x00000010
    SERVICE_ACCEPT_PARAMCHANGE = 0x00000008
    SERVICE_ACCEPT_PAUSE_CONTINUE = 0x00000002
    SERVICE_ACCEPT_PRESHUTDOWN = 0x00000100
    SERVICE_ACCEPT_SHUTDOWN = 0x00000004
    SERVICE_ACCEPT_STOP = 0x00000001
    SERVICE_ACCEPT_HARDWAREPROFILECHANGE = 0x00000020
    SERVICE_ACCEPT_POWEREVENT = 0x00000040
    SERVICE_ACCEPT_SESSIONCHANGE = 0x00000080
    SERVICE_ACCEPT_TIMECHANGE = 0x00000200
    SERVICE_ACCEPT_TRIGGEREVENT = 0x00000400
    SERVICE_ACCEPT_USERMODEREBOOT = 0x00000800

class ServiceType(IntEnum):
    """Windows service manager service type codes"""

    SERVICE_FILE_SYSTEM_DRIVER = 0x00000002
    SERVICE_KERNEL_DRIVER = 0x00000001
    SERVICE_WIN32_OWN_PROCESS = 0x00000010
    SERVICE_WIN32_SHARE_PROCESS = 0x00000020
    SERVICE_USER_OWN_PROCESS = 0x00000050
    SERVICE_USER_SHARE_PROCESS = 0x00000060
    SERVICE_INTERACTIVE_PROCESS = 0x00000100

