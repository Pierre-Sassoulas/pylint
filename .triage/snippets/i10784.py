class Statement:
    pass


class Expression:
    pass


class Assignment(Statement):
    src: Expression


class ConditionalJump(Statement):
    pass


class BinaryOp(Expression):
    op: str


class Block:
    statements: list[Statement]


def make_block_with_conditional_jump() -> Block:
    cond_block = Block()
    cond_block.statements = [ConditionalJump()]
    return cond_block


def check_block_local():
    block = Block()
    for stmt in block.statements:
        if isinstance(stmt, Assignment) and isinstance(stmt.src, BinaryOp):
            print("Assignment")
