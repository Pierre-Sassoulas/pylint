def func(numbers: list[int]) -> int | None:
    if not numbers:
        return None
    for number in numbers:
        if number % 2:
            break
    return number
