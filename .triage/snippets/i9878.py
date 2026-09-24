def testMethod(testString):
    if testString == "option1":
        return 1
    if testString == ("option2"):
        return 2
    if testString in ("option1", "option2"):
        return 3
    if testString in ("option4"):
        return 4
    if testString == "option":
        raise ValueError("Did you forget?")
    return "None of the above"


print(testMethod("option"))
