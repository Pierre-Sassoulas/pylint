"""Module docstring"""
# pylint: disable=invalid-name, too-few-public-methods
# This disable should prevent invalid-name errors from appearing in report_srv_status and init
# ... but it does not
from example_structure import SERVICE_STATUS, ControlsAccepted, CurrentState, ServiceType



class ExampleService:
    """Class showing spurious pylint errors"""

    def __init__(
        self, name: str, display_name: str, desc: str
    ) -> None:
        self.name = name
        self.desc = desc
        self.display_name = display_name
        self._srv_status: SERVICE_STATUS = SERVICE_STATUS()
        self._srv_status.dwServiceType = ServiceType.SERVICE_WIN32_OWN_PROCESS
        self._srv_status.dwServiceSpecificExitCode = 0

    def report_srv_status(self, current_state: int, win32_exit_code: int, wait_hint: int) -> None:
        """
        Notifies the service controller on the state of the service.
        This is required to tell the controller the service has started or stopped.
        """

        # Update the srv_status object with current state of the service
        self._srv_status.dwCurrentState = current_state
        self._srv_status.dwWin32ExitCode = win32_exit_code
        self._srv_status.dwWaitHint = wait_hint

        if current_state == CurrentState.SERVICE_START_PENDING:
            self._srv_status.dwControlsAccepted = 0
        else:
            self._srv_status.dwControlsAccepted = ControlsAccepted.SERVICE_ACCEPT_STOP

        if current_state in (CurrentState.SERVICE_RUNNING, CurrentState.SERVICE_STOPPED):
            self._srv_status.dwCheckPoint= 0
        else:
            self._srv_status.dwCheckPoint += 1

        # Other stuff excluded ....
