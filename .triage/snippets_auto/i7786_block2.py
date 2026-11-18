def _is_property_kind(node: nodes.NodeNG, *kinds: str) -> bool:
    return(
        isinstance(node, (astroid.UnboundMethod, nodes.FunctionDef))
        and node.decorators
        and any(
            isinstance(decorator, nodes.Attribute)
            for decorator in node.decorators.nodes
        )
    )
