d = {
    "status": {
        "a": (
            str(var) if (var := 2) else None  # <-- false-positive
        ),
    }
}
