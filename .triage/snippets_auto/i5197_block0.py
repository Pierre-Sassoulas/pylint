# pylint: disable-next=fixme
# TODO: With better control-flow inference related to NamedExpr we should see that the
# NamedExpr is never called here and the second call to `var` is thus undefined
def typing_and_incorrect_assignment_expression():
    """The variable gets assigned in an assignment expression which is never called"""
    var: int
    if False:
        if (var := 1 ** 2):
            print(var)
    else:
        print(var) # This should raise
