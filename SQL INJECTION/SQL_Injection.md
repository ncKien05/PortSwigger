# SQL Injection
Trong phần này, chúng tôi giải thích:  
* SQL injection (SQLi) là gì?  
* Cách tìm và khai thác các loại lỗ hổng SQLi khác nhau.  
* Làm thế nào để ngăn chặn SQLi.  
## SQL injection (SQLi) là gì?  
* SQL Injection (SQLi) là một lỗ hổng bảo mật web cho phép kẻ tấn công can thiệp vào các truy vấn mà ứng dụng thực hiện đối với cơ sở dữ liệu. Điều này có thể cho phép kẻ tấn công xem dữ liệu mà thông thường chúng không thể truy xuất. Dữ liệu này có thể bao gồm dữ liệu thuộc về người dùng khác hoặc bất kỳ dữ liệu nào khác mà ứng dụng có thể truy cập. Trong nhiều trường hợp, kẻ tấn công có thể sửa đổi hoặc xóa dữ liệu này, gây ra những thay đổi liên tục đối với nội dung hoặc hành vi của ứng dụng.  
  
* Trong một số trường hợp, kẻ tấn công có thể leo thang tấn công SQL injection để xâm nhập máy chủ hoặc cơ sở hạ tầng back-end khác. Điều này cũng có thể cho phép chúng thực hiện các cuộc tấn công từ chối dịch vụ.  
## Tác động của một cuộc tấn công SQL injection thành công là gì?  
Một cuộc tấn công tiêm SQL thành công có thể dẫn đến truy cập trái phép vào dữ liệu nhạy cảm, chẳng hạn như:  
  * Mật khẩu.  
  * Chi tiết thẻ tín dụng.  
  * Thông tin cá nhân của người dùng.  

Các cuộc tấn công tiêm nhiễm SQL đã được sử dụng trong nhiều vụ vi phạm dữ liệu nghiêm trọng trong nhiều năm qua. Chúng đã gây ra thiệt hại về uy tín và các khoản phạt theo quy định. Trong một số trường hợp, kẻ tấn công có thể xâm nhập vào hệ thống của tổ chức, dẫn đến một sự xâm phạm lâu dài mà không bị phát hiện trong một thời gian dài.  
## Cách phát hiện lỗ hổng SQL injection  
Bạn có thể phát hiện SQL Injection theo cách thủ công bằng cách sử dụng một bộ kiểm tra có hệ thống trên mọi điểm vào của ứng dụng. Để làm điều này, bạn thường sẽ gửi:
* Ký tự dấu nháy đơn `'` và tìm kiếm lỗi hoặc các bất thường khác.
* Một số cú pháp SQL cụ thể đánh giá theo giá trị cơ sở (gốc) của điểm vào và theo một giá trị khác, đồng thời tìm kiếm sự khác biệt có hệ thống trong phản hồi của ứng dụng.
* Các điều kiện Boolean như `OR 1=1` và `OR 1=2`  , và tìm kiếm sự khác biệt trong phản hồi của ứng dụng.
* Tải trọng được thiết kế để kích hoạt độ trễ thời gian khi thực hiện trong truy vấn SQL và tìm kiếm sự khác biệt về thời gian phản hồi.  
* Tải trọng OAST được thiết kế để kích hoạt tương tác mạng ngoài băng tần khi được thực hiện trong truy vấn SQL và giám sát mọi tương tác phát sinh.  

Ngoài ra, bạn có thể tìm thấy phần lớn các lỗ hổng SQL injection một cách nhanh chóng và đáng tin cậy bằng Burp Scanner.  

## Tiêm SQL vào các phần khác nhau của truy vấn  
Hầu hết các lỗ hổng SQL injection đều xảy ra trong WHEREmệnh đề của một SELECTtruy vấn. Hầu hết các kiểm thử viên giàu kinh nghiệm đều quen thuộc với loại SQL injection này.  
  
Tuy nhiên, lỗ hổng SQL injection có thể xảy ra ở bất kỳ vị trí nào trong truy vấn và trong nhiều loại truy vấn khác nhau. Một số vị trí phổ biến khác mà SQL injection phát sinh là:  
  
* Trong `UPDATE` các câu lệnh, trong các giá trị được cập nhật hoặc mệnh `WHERE` đề.
* Trong `INSERT` các câu lệnh, bên trong các giá trị được chèn vào.
* Trong `SELECT` các câu lệnh, bên trong tên bảng hoặc cột.
* Trong `SELECT` các câu lệnh, trong `ORDER BY` mệnh đề.
## Truy xuất dữ liệu ẩn  
Hãy tưởng tượng một ứng dụng mua sắm hiển thị sản phẩm theo nhiều danh mục khác nhau. Khi người dùng nhấp vào danh mục Quà tặng , trình duyệt của họ sẽ yêu cầu URL:  
`https://insecure-website.com/products?category=Gifts`  
Điều này khiến ứng dụng thực hiện truy vấn SQL để lấy thông tin chi tiết về các sản phẩm có liên quan từ cơ sở dữ liệu:  
`SELECT * FROM products WHERE category = 'Gifts' AND released = 1`  

Truy vấn SQL này yêu cầu cơ sở dữ liệu trả về:  
* tất cả các chi tiết ( *)
* từ bảng product
* nơi category = Gifts
* và released = 1.  
Hạn chế này `released = 1` được sử dụng để ẩn các sản phẩm chưa được phát hành. Chúng ta có thể giả định đối với các sản phẩm chưa được phát hành, `released = 0`

Ứng dụng không triển khai bất kỳ biện pháp phòng thủ nào chống lại các cuộc tấn công SQL injection. Điều này có nghĩa là kẻ tấn công có thể thực hiện các cuộc tấn công sau, ví dụ:  
`https://insecure-website.com/products?category=Gifts'--`  

Điều này dẫn đến truy vấn SQL:  
`SELECT * FROM products WHERE category = 'Gifts'--' AND released = 1`  

Quan trọng hơn, hãy lưu ý rằng đây `--` là một chỉ báo chú thích trong SQL. Điều này có nghĩa là phần còn lại của truy vấn được hiểu là một chú thích, về cơ bản là loại bỏ nó. Trong ví dụ này, điều này có nghĩa là truy vấn không còn chứa `AND released = 1`. Kết quả là, tất cả các sản phẩm đều được hiển thị, bao gồm cả những sản phẩm chưa được phát hành.  

Bạn có thể sử dụng một cuộc tấn công tương tự để khiến ứng dụng hiển thị tất cả các sản phẩm trong bất kỳ danh mục nào, bao gồm cả những danh mục mà ứng dụng không biết:  

`https://insecure-website.com/products?category=Gifts'+OR+1=1--`  

Điều này dẫn đến truy vấn SQL:

`SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1`  

* Cảnh báo:  
Hãy cẩn thận khi chèn điều kiện `OR 1=1` vào truy vấn SQL. Ngay cả khi điều kiện có vẻ vô hại trong ngữ cảnh bạn đang chèn, các ứng dụng thường sử dụng dữ liệu từ một yêu cầu duy nhất trong nhiều truy vấn khác nhau. Ví dụ: nếu điều kiện của bạn đạt đến câu lệnh `UPDATE` hoặc `DELETE`, điều đó có thể dẫn đến mất dữ liệu ngoài ý muốn.  
### Phòng thí nghiệm: Lỗ hổng SQL injection trong mệnh đề WHERE cho phép truy xuất dữ liệu ẩn
[Solution]("./lab1.py")