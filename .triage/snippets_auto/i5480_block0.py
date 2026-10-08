from typing import List


def parse_dict(dict_object: List[dict], name: str) -> dict:
    for dict in dict_object:
        if dict.get("name") == name:
            return dict
    return {}
