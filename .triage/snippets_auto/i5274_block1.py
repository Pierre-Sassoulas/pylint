def register(linter):
    original = VariablesChecker.add_message

    def _new_add_message(
        self, msgid, line = None, node = None, args= None, confidence= None, col_offset= None,
    ):
        if (
            msgid == "unused-argument"
            and isinstance(node, AssignName)
            and node.name == "context"
            and isinstance(node.parent, Arguments)
            and isinstance(node.parent.parent, FunctionDef)
            and "invoke.tasks.task" in node.parent.parent.decoratornames()
        ):
            return
        original(self, msgid, line, node, args, confidence, col_offset)

    VariablesChecker.add_message = _new_add_message
