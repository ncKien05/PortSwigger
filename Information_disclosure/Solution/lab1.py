import requests

target_url = "http://YOUR_HOST/"

payload="product?productId=1`"

res=requests.get(target_url+payload)
print(res.status_code)
print(res.text)