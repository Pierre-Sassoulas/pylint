def sequence_match_statement():
    """ Test matching the first element of a sequence is a frog. """
    seq = ["🐸", "🐛", "🦋", "🪲"]
    frogs = 0
    for _ in range(100_000):
        match seq:
            case ["🐸", *_]: frogs += 1
    
    assert frogs == 100_000
