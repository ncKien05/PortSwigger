# Tấn công SQL injection UNION
Khi một ứng dụng dễ bị tấn công SQL injection, và kết quả truy vấn được trả về trong phản hồi của ứng dụng, bạn có thể sử dụng `UNION` từ khóa để truy xuất dữ liệu từ các bảng khác trong cơ sở dữ liệu. Điều này thường được gọi là tấn công SQL injection UNION.  
Từ khóa này `UNION` cho phép bạn thực hiện một hoặc nhiều `SELECT` truy vấn bổ sung và thêm kết quả vào truy vấn ban đầu. Ví dụ:  
`SELECT a, b FROM table1 UNION SELECT c, d FROM table2`  
Truy vấn SQL này trả về một tập kết quả duy nhất với hai cột, chứa các giá trị từ các cột `a` và `b` trong `table1` và các cột `c` và `d` trong `table2`.

Để `UNION` truy vấn hoạt động, cần đáp ứng hai yêu cầu chính:

* Các truy vấn riêng lẻ phải trả về cùng số lượng cột.  
* Các kiểu dữ liệu trong mỗi cột phải tương thích giữa các truy vấn riêng lẻ.  

Để thực hiện tấn công SQL injection UNION, hãy đảm bảo cuộc tấn công của bạn đáp ứng hai yêu cầu này. Điều này thường bao gồm việc tìm hiểu:  
* Truy vấn ban đầu trả về bao nhiêu cột?  
* Những cột nào được trả về từ truy vấn gốc có kiểu dữ liệu phù hợp để chứa kết quả từ truy vấn được chèn vào?  

# Xác định số lượng cột cần thiết
Khi thực hiện tấn công SQL injection UNION, có hai phương pháp hiệu quả để xác định số lượng cột được trả về từ truy vấn gốc.  

Một phương pháp là chèn một loạt `ORDER BY` các mệnh đề và tăng chỉ số cột được chỉ định cho đến khi xảy ra lỗi. Ví dụ, nếu điểm chèn là một chuỗi được đặt trong dấu ngoặc kép bên trong mệnh `WHERE` đề của truy vấn gốc, bạn sẽ gửi:  
```
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
etc.
```  
Chuỗi tải trọng này sửa đổi truy vấn gốc để sắp xếp kết quả theo các cột khác nhau trong tập kết quả. Cột trong mệnh `ORDER BY` đề có thể được chỉ định bằng chỉ mục của nó, vì vậy bạn không cần biết tên của bất kỳ cột nào. Khi chỉ mục cột được chỉ định vượt quá số lượng cột thực tế trong tập kết quả, cơ sở dữ liệu sẽ trả về lỗi, ví dụ:  
`The ORDER BY position number 3 is out of range of the number of items in the select list.`  
Ứng dụng có thể thực sự trả về lỗi cơ sở dữ liệu trong phản hồi HTTP của nó, nhưng nó cũng có thể đưa ra một phản hồi lỗi chung chung. Trong những trường hợp khác, nó có thể đơn giản là không trả về kết quả nào cả. Dù bằng cách nào, miễn là bạn có thể phát hiện ra một số khác biệt trong phản hồi, bạn có thể suy ra có bao nhiêu cột đang được trả về từ truy vấn.  
Phương pháp thứ hai liên quan đến việc gửi một loạt `UNION SELECT` các gói dữ liệu chỉ định số lượng giá trị null khác nhau:  
```
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
etc.
```
Nếu số lượng giá trị null không khớp với số lượng cột, cơ sở dữ liệu sẽ trả về lỗi, ví dụ như:  
`All queries combined using a UNION, INTERSECT or EXCEPT operator must have an equal number of expressions in their target lists.`  
Chúng tôi sử dụng `NULL` các giá trị trả về từ truy `SELECT` vấn được chèn vì kiểu dữ liệu trong mỗi cột phải tương thích giữa truy vấn gốc và truy vấn được chèn. `NULL` Kiểu dữ liệu này có thể chuyển đổi sang mọi kiểu dữ liệu phổ biến, do đó nó tối đa hóa khả năng thành công của tải trọng khi số lượng cột chính xác.  
Cũng giống như `ORDER BY` kỹ thuật này, ứng dụng có thể thực sự trả về lỗi cơ sở dữ liệu trong phản hồi HTTP của nó, nhưng có thể trả về lỗi chung chung hoặc đơn giản là không trả về kết quả nào. Khi số lượng giá trị null khớp với số lượng cột, cơ sở dữ liệu sẽ trả về một hàng bổ sung trong tập kết quả, chứa các giá trị null trong mỗi cột. Ảnh hưởng đến phản hồi HTTP phụ thuộc vào mã của ứng dụng. Nếu may mắn, bạn sẽ thấy một số nội dung bổ sung trong phản hồi, chẳng hạn như một hàng bổ sung trên bảng HTML. Nếu không, các giá trị null có thể gây ra một lỗi khác, chẳng hạn như lỗi `NullPointerException` . Trong trường hợp xấu nhất, phản hồi có thể trông giống như phản hồi do số lượng giá trị null không chính xác gây ra. Điều này sẽ làm cho phương pháp này không hiệu quả.  
## Bài thực hành: Tấn công SQL injection UNION, xác định số lượng cột được trả về bởi truy vấn.  
[SOLUTION](./solution/lab8.PY)
# Cú pháp dành riêng cho cơ sở dữ liệu  
Trên Oracle, mọi `SELECT` truy vấn đều phải sử dụng `FROM` từ khóa và chỉ định một bảng hợp lệ. Có một bảng tích hợp sẵn trên Oracle có tên là `<table>` `dual` có thể được sử dụng cho mục đích này. Vì vậy, các truy vấn được chèn vào Oracle sẽ cần có dạng như sau:  
`' UNION SELECT NULL FROM DUAL--`  
Các payload được mô tả sử dụng chuỗi chú thích hai dấu gạch ngang `--` để vô hiệu hóa phần còn lại của truy vấn gốc sau điểm chèn. Trên MySQL, chuỗi hai dấu gạch ngang phải được theo sau bởi một khoảng trắng. Ngoài ra, ký tự dấu thăng `#` cũng có thể được sử dụng để xác định một chú thích.  

# Tìm các cột có kiểu dữ liệu hữu ích  
Tấn công SQL injection UNION cho phép bạn truy xuất kết quả từ một truy vấn bị chèn. Dữ liệu cần truy xuất thường ở dạng chuỗi. Điều này có nghĩa là bạn cần tìm một hoặc nhiều cột trong kết quả truy vấn gốc có kiểu dữ liệu là, hoặc tương thích với, dữ liệu chuỗi.  
Sau khi xác định số lượng cột cần thiết, bạn có thể kiểm tra từng cột để xem liệu nó có thể chứa dữ liệu chuỗi hay không. Bạn có thể gửi một loạt `UNION SELECT` các payload để đặt giá trị chuỗi vào từng cột một. Ví dụ, nếu truy vấn trả về bốn cột, bạn sẽ gửi:  
```
' UNION SELECT 'a',NULL,NULL,NULL--
' UNION SELECT NULL,'a',NULL,NULL--
' UNION SELECT NULL,NULL,'a',NULL--
' UNION SELECT NULL,NULL,NULL,'a'--
```  
Nếu kiểu dữ liệu của cột không tương thích với dữ liệu chuỗi, truy vấn được chèn sẽ gây ra lỗi cơ sở dữ liệu, ví dụ như:  
`Conversion failed when converting the varchar value 'a' to data type int.`  
Nếu không xảy ra lỗi và phản hồi của ứng dụng chứa một số nội dung bổ sung bao gồm giá trị chuỗi được chèn, thì cột liên quan phù hợp để truy xuất dữ liệu chuỗi.  
## Bài thực hành: Tấn công SQL injection UNION, tìm cột chứa văn bản.  
[SOLUTION](./solution/lab9.py)
# Sử dụng tấn công SQL injection UNION để lấy dữ liệu thú vị.  
Khi bạn đã xác định được số lượng cột được trả về bởi truy vấn ban đầu và tìm ra những cột có thể chứa dữ liệu chuỗi, bạn đã có thể truy xuất dữ liệu cần thiết.  
Giả sử rằng:  
* Truy vấn ban đầu trả về hai cột, cả hai đều có thể chứa dữ liệu dạng chuỗi.
* Điểm chèn là một chuỗi được đặt trong dấu ngoặc kép bên trong mệnh `WHERE` đề.
* Cơ sở dữ liệu chứa một bảng có tên là `users` với các cột `username` và `password`.  
Trong ví dụ này, bạn có thể truy xuất nội dung của `users` bảng bằng cách nhập dữ liệu:  
`' UNION SELECT username, password FROM users--`  
Để thực hiện cuộc tấn công này, bạn cần biết rằng có một bảng có tên là `users` với hai cột có tên là `username` và `password`. Nếu không có thông tin này, bạn sẽ phải đoán tên của các bảng và cột. Tất cả các cơ sở dữ liệu hiện đại đều cung cấp các cách để kiểm tra cấu trúc cơ sở dữ liệu và xác định các bảng và cột mà chúng chứa.  
## Bài thực hành: Tấn công SQL injection UNION, truy xuất dữ liệu từ các bảng khác. 
 
# Truy xuất nhiều giá trị trong cùng một cột  
Trong một số trường hợp, truy vấn trong ví dụ trước có thể chỉ trả về một cột duy nhất.  
Bạn có thể truy xuất nhiều giá trị cùng lúc trong một cột duy nhất bằng cách nối các giá trị lại với nhau. Bạn có thể thêm dấu phân cách để phân biệt các giá trị đã kết hợp. Ví dụ, trên Oracle, bạn có thể nhập dữ liệu như sau:  
`' UNION SELECT username || '~' || password FROM users--`  
Phương pháp này sử dụng chuỗi dấu gạch dọc kép `||` , là một toán tử nối chuỗi trên Oracle. Truy vấn được chèn sẽ nối các giá trị của trường `usernameand` lại với nhau `password` , được phân tách bởi `~` ký tự `<`.  
Kết quả truy vấn bao gồm tất cả tên người dùng và mật khẩu, ví dụ:  
```
...
administrator~s3cure
wiener~peter
carlos~montoya
...
```  
Các cơ sở dữ liệu khác nhau sử dụng cú pháp khác nhau để thực hiện nối chuỗi.  
## Bài thực hành: Tấn công SQL injection UNION, truy xuất nhiều giá trị trong một cột duy nhất.
  