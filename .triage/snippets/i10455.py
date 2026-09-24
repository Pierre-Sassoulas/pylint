from typing import Any


def use(structs1: dict, structs2: dict) -> Any:
    end_of_good_plan = structs1["<key>"] if "<key>" in structs1 else None
    end_of_bad_plan = structs2["<key>"] if "<key>" in structs2 else None

    if end_of_good_plan is not None and end_of_bad_plan is not None:
        return end_of_good_plan[0]
    return None
