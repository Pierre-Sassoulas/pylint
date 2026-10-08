"""cell-var-from-loop example."""

grouped_messages = {
    "category_a": [
        {"key_a": 3},
        {"key_a": 1},
        {"key_a": 2},
    ],
    "category_b": [
        {"key_b": 5},
        {"key_b": 3},
        {"key_b": 8},
    ],
}
sorting_keys = {
    "category_a": "key_a",
    "category_b": "key_b",
}

sorted_messages = {}

for category, messages in grouped_messages.items():
    sorted_messages[category] = sorted(
        (message for message in messages),
        key=lambda msg: msg[sorting_keys[category]]
    )

print(sorted_messages)
