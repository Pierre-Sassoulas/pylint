class MessageVariant:
    message: str

    def __init__(self, message: str) -> None:
        self.message = message


class OtherVariant:
    pass


def parse(operation: str) -> MessageVariant | OtherVariant:
    if operation != "":
        return MessageVariant(operation)
    return OtherVariant()


def edit_messages(operation: str) -> None:
    variant = parse(operation)
    if isinstance(variant, MessageVariant):
        # W0201: Attribute 'message' defined outside __init__ (attribute-defined-outside-init)
        variant.message = ""
