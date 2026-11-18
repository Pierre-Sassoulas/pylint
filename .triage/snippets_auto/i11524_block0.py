import astroid
from pylint.checkers.utils import get_argument_from_call

result = get_argument_from_call(astroid.extract_node("f(1)"), 0)
print(type(result).__name__)  # Const; declared return type: nodes.Name
