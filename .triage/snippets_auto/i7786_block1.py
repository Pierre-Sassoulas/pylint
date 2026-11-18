def _is_property_kind(node: nodes.NodeNG, *kinds: str) -> bool:
    if not isinstance(node, (astroid.UnboundMethod, nodes.FunctionDef)):
        return False
    if node.decorators:
        ########################################
        if any(
	    isinstance(decorator, nodes.Attribute) and decorator.attrname in kinds
	    for decorator in node.decorators.nodes
	):
            return True
	########################################
    return False
