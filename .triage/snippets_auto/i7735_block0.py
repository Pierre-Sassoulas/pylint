match x:
    case "foo":
        from app.foo import foo
        print("foo")

    case "api":
        import something_else
        from app.api import app
        # do something with the app
