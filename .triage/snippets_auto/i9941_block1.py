import requests

try:
    response = requests.get("https://google.com", timeout=1) 
    response2 = response
except Exception:
    print(response) # should still raise used-before-assignment

