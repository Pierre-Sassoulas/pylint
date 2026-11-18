def _is_property_kind(node: nodes.NodeNG, *kinds: str) -> bool:
    if not isinstance(node, (astroid.UnboundMethod, nodes.FunctionDef)):
        return False
    if node.decorators:
        for decorator in node.decorators.nodes:
            if isinstance(decorator, nodes.Attribute) and decorator.attrname in kinds:
                return True
    return False
