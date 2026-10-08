import random

results= [
    {"name": "cheri", "url": "https://pokeapi.co/api/v2/berry/1/"},
    {"name": "chesto", "url": "https://pokeapi.co/api/v2/berry/2/"}
]

items: list[dict[str, str]] = random.sample(results, 5)
for item in items:
    b = item["url"]
