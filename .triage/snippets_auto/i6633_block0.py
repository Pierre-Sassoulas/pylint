def sequence_match_logical():
    """ Test matching the first element of a sequence is a frog. """
    seq = ["🐸", "🐛", "🦋", "🪲"]
    frogs = 0
    for _ in range(100_000):
        if isinstance(seq, Sequence) and len(seq) > 0 and seq[0] == "🐸": 
            frogs += 1
    
    assert frogs == 100_000
