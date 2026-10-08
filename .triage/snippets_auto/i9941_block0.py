import requests

try:
    response = requests.get("https://google.com", timeout=1)
except Exception:
    print(response) # correctly raises used-before-assignment
