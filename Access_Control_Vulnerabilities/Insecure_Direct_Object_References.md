# Tham chiếu đối tượng trực tiếp không an toàn (IDOR)  
Trong phần này, chúng ta sẽ giải thích tham chiếu đối tượng trực tiếp không an toàn (IDOR) là gì và mô tả một số lỗ hổng phổ biến.  

# Tham chiếu đối tượng trực tiếp không an toàn (IDOR) là gì?  
Lỗ hổng tham chiếu trực tiếp đối tượng không an toàn (IDOR) là một loại lỗ hổng kiểm soát truy cập phát sinh khi ứng dụng sử dụng dữ liệu do người dùng cung cấp để truy cập trực tiếp vào các đối tượng. Thuật ngữ IDOR trở nên phổ biến nhờ sự xuất hiện của nó trong danh sách Top Ten của OWASP năm 2007. Tuy nhiên, đây chỉ là một ví dụ trong số nhiều lỗi triển khai kiểm soát truy cập có thể dẫn đến việc bị vượt qua các biện pháp kiểm soát truy cập. Lỗ hổng IDOR thường liên quan đến leo thang đặc quyền theo chiều ngang, nhưng chúng cũng có thể phát sinh liên quan đến leo thang đặc quyền theo chiều dọc.  

# Ví dụ về IDOR  
Có rất nhiều ví dụ về các lỗ hổng bảo mật trong đó các giá trị tham số do người dùng thiết lập được sử dụng để truy cập trực tiếp vào tài nguyên hoặc chức năng.  

## Lỗ hổng IDOR liên quan trực tiếp đến các đối tượng cơ sở dữ liệu  
Hãy xem xét một trang web sử dụng URL sau để truy cập trang tài khoản khách hàng, bằng cách lấy thông tin từ cơ sở dữ liệu phía máy chủ:  
`https://insecure-website.com/customer_account?customer_number=132355`  

Ở đây, số khách hàng được sử dụng trực tiếp làm chỉ mục bản ghi trong các truy vấn được thực hiện trên cơ sở dữ liệu phía máy chủ. Nếu không có biện pháp kiểm soát nào khác, kẻ tấn công có thể dễ dàng sửa đổi giá trị `customer_number`, vượt qua các biện pháp kiểm soát truy cập để xem hồ sơ của các khách hàng khác. Đây là một ví dụ về lỗ hổng IDOR dẫn đến leo thang đặc quyền theo chiều ngang.

Kẻ tấn công có thể thực hiện leo thang đặc quyền theo chiều ngang và chiều dọc bằng cách thay đổi người dùng thành người dùng có thêm đặc quyền trong khi vượt qua các biện pháp kiểm soát truy cập. Các khả năng khác bao gồm khai thác lỗ hổng rò rỉ mật khẩu hoặc sửa đổi các tham số sau khi kẻ tấn công đã truy cập được vào trang tài khoản của người dùng, chẳng hạn.  

## Lỗ hổng IDOR liên quan trực tiếp đến các tập tin tĩnh.  
Lỗ hổng IDOR thường phát sinh khi các tài nguyên nhạy cảm được lưu trữ trong các tệp tĩnh trên hệ thống tệp phía máy chủ. Ví dụ, một trang web có thể lưu bản ghi tin nhắn trò chuyện vào ổ đĩa bằng tên tệp tăng dần và cho phép người dùng truy xuất chúng bằng cách truy cập URL như sau:  
`https://insecure-website.com/static/12144.txt`  

Trong trường hợp này, kẻ tấn công có thể dễ dàng thay đổi tên tệp để lấy được bản ghi do người dùng khác tạo ra và có khả năng thu thập thông tin đăng nhập của người dùng cũng như các dữ liệu nhạy cảm khác.  

### Bài thực hành: Tham chiếu đối tượng trực tiếp không an toàn  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab11.py)
