"""Miss-leading Pylint no name in module error"""

from unicon.core.errors import ConnectionError as UniconConnectionError

raise UniconConnectionError()
