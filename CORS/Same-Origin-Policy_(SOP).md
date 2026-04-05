# Chính sách cùng nguồn gốc (SOP)  
Trong phần này, chúng tôi sẽ giải thích chính sách cùng nguồn gốc (SOP) là gì và cách thức thực hiện chính sách này.  

# Chính sách cùng nguồn gốc là gì?  
Chính sách cùng nguồn gốc là một cơ chế bảo mật của trình duyệt web nhằm ngăn chặn các trang web tấn công lẫn nhau.

Chính sách cùng nguồn gốc hạn chế các tập lệnh trên một nguồn gốc truy cập dữ liệu từ một nguồn gốc khác. Một nguồn gốc bao gồm lược đồ URI, tên miền và số cổng. Ví dụ, hãy xem xét URL sau:  
`http://normal-website.com/example/example.html`  

Phương thức này sử dụng lược đồ `http`, tên miền `normal-website.com` và số cổng `80`. Bảng sau đây cho thấy chính sách cùng nguồn gốc sẽ được áp dụng như thế nào nếu nội dung tại URL trên cố gắng truy cập các nguồn gốc khác:  
| URL đã truy cập | Được phép truy cập? |
| :--- | :--- |
| `http://normal-website.com/example/` | **Đúng:** cùng lược đồ, tên miền và cổng. |
| `http://normal-website.com/example2/` | **Đúng:** cùng lược đồ, tên miền và cổng. |
| `https://normal-website.com/example/` | **Không:** sơ đồ và cổng khác |
| `http://en.normal-website.com/example/` | **Không:** miền khác |
| `http://www.normal-website.com/example/` | **Không:** miền khác |
| `http://normal-website.com:8080/example/` | **Không:** cổng khác* |  

*Internet Explorer sẽ cho phép truy cập này vì IE không tính đến số cổng khi áp dụng chính sách cùng nguồn gốc.  
# Tại sao chính sách cùng nguồn gốc lại cần thiết?  
Khi trình duyệt gửi yêu cầu HTTP từ một nguồn gốc này đến một nguồn gốc khác, bất kỳ cookie nào, bao gồm cả cookie phiên xác thực, liên quan đến miền kia cũng được gửi kèm theo yêu cầu. Điều này có nghĩa là phản hồi sẽ được tạo ra trong phiên của người dùng và bao gồm bất kỳ dữ liệu liên quan nào cụ thể cho người dùng đó. Nếu không có chính sách cùng nguồn gốc, nếu bạn truy cập vào một trang web độc hại, nó có thể đọc được email của bạn từ Gmail, tin nhắn riêng tư từ Facebook, v.v.  
# Chính sách cùng nguồn gốc được thực hiện như thế nào?  
Chính sách cùng nguồn gốc (SOP) thường kiểm soát quyền truy cập của mã JavaScript vào nội dung được tải từ miền khác. Việc tải tài nguyên trang từ nguồn gốc khác thường được cho phép. Ví dụ, SOP cho phép nhúng hình ảnh thông qua thẻ `<img>`, phương tiện truyền thông thông qua thẻ `<video>` và JavaScript thông qua thẻ `<script>`. Tuy nhiên, mặc dù các tài nguyên bên ngoài này có thể được trang tải, bất kỳ mã JavaScript nào trên trang đó cũng không thể đọc nội dung của các tài nguyên này.

Có một số trường hợp ngoại lệ đối với chính sách cùng nguồn gốc:

Một số đối tượng có thể ghi được nhưng không thể đọc được ở miền khác, chẳng hạn như đối tượng `location` hoặc thuộc tính `location.href` từ iframe hoặc cửa sổ mới.
Một số đối tượng có thể đọc được nhưng không thể ghi được giữa các miền khác nhau, chẳng hạn như thuộc tính `length` của đối tượng `window` (lưu trữ số lượng khung hình đang được sử dụng trên trang) và thuộc tính `closed` khác.
Chức năng này `replace` nói chung có thể được gọi xuyên miền trên đối tượng `location`.
Bạn có thể gọi một số hàm khác miền. Ví dụ, bạn có thể gọi các hàm `close`, `blur` và `focus` trong một cửa sổ mới. Hàm `postMessage` cũng có thể được gọi trong iframe và cửa sổ mới để gửi thông báo từ miền này sang miền khác.
Do các yêu cầu cũ, chính sách cùng nguồn gốc được nới lỏng hơn khi xử lý cookie, vì vậy chúng thường có thể truy cập được từ tất cả các tên miền phụ của một trang web ngay cả khi mỗi tên miền phụ về mặt kỹ thuật là một nguồn gốc khác nhau. Bạn có thể giảm thiểu một phần rủi ro này bằng cách sử dụng cờ cookie `HttpOnly`.

Có thể nới lỏng chính sách cùng nguồn gốc (SOP) bằng cách sử dụng thuộc tính `document.domain` đặc biệt này. Thuộc tính này cho phép bạn nới lỏng SOP cho một tên miền cụ thể, nhưng chỉ khi nó là một phần của tên miền đủ điều kiện (FQDN) của bạn. Ví dụ, bạn có một tên miền `marketing.example.com` và bạn muốn đọc nội dung của tên miền đó trên `example.com`. Để làm như vậy, cả hai tên miền cần đặt thuộc tính `document.domain` thành `example.com`. Khi đó, SOP sẽ cho phép truy cập giữa hai tên miền bất chấp nguồn gốc khác nhau của chúng. Trước đây, có thể đặt thuộc tính `document.domain` thành một TLD như `com`, cho phép truy cập giữa bất kỳ tên miền nào trên cùng một TLD, nhưng hiện nay các trình duyệt hiện đại ngăn chặn điều này.