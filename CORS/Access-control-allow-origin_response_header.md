# CORS và tiêu đề phản hồi Access-Control-Allow-Origin  
Trong phần này, chúng tôi sẽ giải thích `Access-Control-Allow-Origin` header là gì liên quan đến CORS và cách nó trở thành một phần của quá trình triển khai CORS.

Đặc tả chia sẻ tài nguyên đa nguồn gốc (cross-origin resource sharing - CRS ) cung cấp sự nới lỏng có kiểm soát đối với chính sách cùng nguồn gốc (same-origin policy) cho các yêu cầu HTTP đến một tên miền trang web này từ một tên miền trang web khác thông qua việc sử dụng một tập hợp các tiêu đề HTTP. Trình duyệt cho phép truy cập vào các phản hồi cho các yêu cầu đa nguồn gốc dựa trên các hướng dẫn trong tiêu đề này.  

# Tiêu đề phản hồi Access-Control-Allow-Origin là gì?  
Tiêu đề này `Access-Control-Allow-Origin` được bao gồm trong phản hồi từ một trang web đối với yêu cầu bắt nguồn từ một trang web khác, và xác định nguồn gốc được cho phép của yêu cầu. Trình duyệt web so sánh `Access-Control-Allow-Origin` với nguồn gốc của trang web yêu cầu và cho phép truy cập vào phản hồi nếu chúng trùng khớp.  
# Thực hiện chia sẻ tài nguyên đa nguồn gốc đơn giản  
Đặc tả chia sẻ tài nguyên đa nguồn gốc (CORS) quy định nội dung tiêu đề được trao đổi giữa máy chủ web và trình duyệt nhằm hạn chế nguồn gốc của các yêu cầu tài nguyên web nằm ngoài miền gốc. Đặc tả CORS xác định một tập hợp các tiêu đề giao thức, trong đó `Access-Control-Allow-Origin` tiêu đề quan trọng nhất là tiêu đề này. Tiêu đề này được máy chủ trả về khi một trang web yêu cầu tài nguyên đa miền, kèm theo một `Origin` tiêu đề khác được trình duyệt thêm vào.

Ví dụ, giả sử một trang web có nguồn gốc `normal-website.com` gây ra yêu cầu liên miền sau:  
```
GET /data HTTP/1.1
Host: robust-website.com
Origin : https://normal-website.com
```
Máy chủ `robust-website.com` trả về phản hồi sau:  
```
HTTP/1.1 200 OK
...
Access-Control-Allow-Origin: https://normal-website.com
```
Trình duyệt sẽ cho phép mã đang chạy `normal-website.com` truy cập phản hồi vì nguồn gốc trùng khớp.

Thông số kỹ thuật `Access-Control-Allow-Origin` cho phép nhiều nguồn gốc, hoặc giá trị `null`, hoặc ký tự đại diện `*`. Tuy nhiên, không có trình duyệt nào hỗ trợ nhiều nguồn gốc và có những hạn chế khi sử dụng ký tự đại diện `*`.  

# Xử lý các yêu cầu tài nguyên từ nhiều nguồn khác nhau kèm theo thông tin xác thực.  

Theo mặc định, các yêu cầu tài nguyên đa nguồn gốc (CORS) sẽ được chuyển tiếp mà không cần thông tin xác thực như cookie và tiêu đề Authorization. Tuy nhiên, máy chủ đa miền có thể cho phép đọc phản hồi khi có thông tin xác thực được truyền đến bằng cách đặt `Access-Control-Allow-Credentials` tiêu đề CORS thành true. Bây giờ, nếu trang web yêu cầu sử dụng JavaScript để khai báo rằng nó đang gửi cookie cùng với yêu cầu:  
```
GET /data HTTP/1.1
Host: robust-website.com
...
Origin: https://normal-website.com
Cookie: JSESSIONID=<value>
```

Và câu trả lời cho yêu cầu đó là:  
```
HTTP/1.1 200 OK
...
Access-Control-Allow-Origin: https://normal-website.com
Access-Control-Allow-Credentials: true
```  

Khi đó, trình duyệt sẽ cho phép trang web yêu cầu đọc phản hồi, vì `Access-Control-Allow-Credentials` tiêu đề phản hồi được đặt thành `true`. Ngược lại, trình duyệt sẽ không cho phép truy cập vào phản hồi.  

# Việc nới lỏng các quy định CORS bằng cách sử dụng ký tự đại diện  

Phần tiêu đề `Access-Control-Allow-Origin` hỗ trợ ký tự đại diện. Ví dụ:  
`Access-Control-Allow-Origin: *`  

Lưu ý rằng ký tự đại diện không thể được sử dụng bên trong bất kỳ giá trị nào khác. Ví dụ, tiêu đề sau đây không hợp lệ:  
`Access-Control-Allow-Origin: https://*.normal-website.com`  

May mắn thay, từ góc độ bảo mật, việc sử dụng ký tự đại diện bị hạn chế trong đặc tả vì bạn không thể kết hợp ký tự đại diện với việc truyền thông tin xác thực giữa các nguồn gốc khác nhau (xác thực, cookie hoặc chứng chỉ phía máy khách). Do đó, phản hồi của máy chủ liên miền có dạng:  
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

Điều này không được phép vì sẽ tiềm ẩn nguy cơ mất an ninh nghiêm trọng, làm lộ bất kỳ nội dung đã được xác thực nào trên trang web mục tiêu cho tất cả mọi người.

Với những hạn chế này, một số máy chủ web tạo ra `Access-Control-Allow-Origin` các tiêu đề một cách động dựa trên nguồn gốc do máy khách chỉ định. Đây là một giải pháp tạm thời cho các hạn chế CORS nhưng không an toàn. Chúng tôi sẽ chỉ cho bạn cách thức khai thác lỗ hổng này ở phần sau.  

# Pre-flight checks  
Kiểm tra trước khi thực hiện yêu cầu (pre-flight check) được thêm vào đặc tả CORS để bảo vệ các tài nguyên cũ khỏi các tùy chọn yêu cầu mở rộng được cho phép bởi CORS. Trong một số trường hợp nhất định, khi một yêu cầu liên miền bao gồm một phương thức hoặc tiêu đề HTTP không chuẩn, yêu cầu liên nguồn gốc sẽ được bắt đầu bằng một yêu cầu sử dụng `OPTIONS` phương thức đó, và giao thức CORS yêu cầu kiểm tra ban đầu về các phương thức và tiêu đề nào được cho phép trước khi cho phép yêu cầu liên nguồn gốc. Điều này được gọi là kiểm tra trước khi thực hiện yêu cầu (pre-flight check). Máy chủ trả về một danh sách các phương thức được cho phép ngoài nguồn gốc đáng tin cậy và trình duyệt kiểm tra xem phương thức của trang web yêu cầu có được cho phép hay không.

Ví dụ, đây là một yêu cầu trước chuyến bay, nhằm mục đích sử dụng `PUT` phương thức này cùng với một tiêu đề yêu cầu tùy chỉnh có tên là `Special-Request-Header`:  
```
OPTIONS /data HTTP/1.1
Host: <some website>
...
Origin: https://normal-website.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: Special-Request-Header
```  

Máy chủ có thể trả về phản hồi như sau:  
```
HTTP/1.1 204 No Content
...
Access-Control-Allow-Origin: https://normal-website.com
Access-Control-Allow-Methods: PUT, POST, OPTIONS
Access-Control-Allow-Headers: Special-Request-Header
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 240
```  
Phản hồi này nêu rõ các phương thức được cho phép ( `PUT`, `POST`, `OPTIONS`) và các tiêu đề yêu cầu được cho phép ( `Special-Request-Header`). Trong trường hợp cụ thể này, máy chủ liên miền cũng cho phép gửi thông tin xác thực, và `Access-Control-Max-Age` tiêu đề xác định khung thời gian tối đa để lưu trữ phản hồi kiểm tra trước khi gửi để sử dụng lại. Nếu các phương thức yêu cầu và tiêu đề được cho phép (như trong ví dụ này) thì trình duyệt sẽ xử lý yêu cầu liên nguồn gốc theo cách thông thường. Kiểm tra trước khi gửi thêm một lượt gửi yêu cầu HTTP bổ sung vào yêu cầu liên miền, do đó chúng làm tăng chi phí duyệt web.  
# CORS có bảo vệ chống lại tấn công CSRF không?  
CORS không cung cấp khả năng bảo vệ chống lại các cuộc tấn công giả mạo yêu cầu xuyên trang (CSRF), đây là một quan niệm sai lầm phổ biến.

CORS là một hình thức nới lỏng có kiểm soát đối với chính sách cùng nguồn gốc, vì vậy việc cấu hình CORS kém có thể làm tăng khả năng xảy ra các cuộc tấn công CSRF hoặc làm trầm trọng thêm tác động của chúng.

Có nhiều cách để thực hiện các cuộc tấn công CSRF mà không cần sử dụng CORS, bao gồm các biểu mẫu HTML đơn giản và việc chèn tài nguyên từ các miền khác nhau.  

