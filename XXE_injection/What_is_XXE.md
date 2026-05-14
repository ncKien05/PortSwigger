# What is XML external entity injection
Lỗ hổng tấn công chèn thực thể ngoại lai XML (còn gọi là XXE) là một lỗ hổng bảo mật web cho phép kẻ tấn công can thiệp vào quá trình xử lý dữ liệu XML của ứng dụng. Nó thường cho phép kẻ tấn công xem các tệp trên hệ thống tệp của máy chủ ứng dụng và tương tác với bất kỳ hệ thống phụ trợ hoặc hệ thống bên ngoài nào mà chính ứng dụng có thể truy cập.  

Trong một số trường hợp, kẻ tấn công có thể leo thang cuộc tấn công XXE để xâm phạm máy chủ hoặc cơ sở hạ tầng phụ trợ khác bằng cách lợi dụng lỗ hổng XXE để thực hiện các cuộc tấn công giả mạo yêu cầu phía máy chủ (SSRF).  

# Các lỗ hổng XXE phát sinh như thế nào?
Một số ứng dụng sử dụng định dạng XML để truyền dữ liệu giữa trình duyệt và máy chủ. Các ứng dụng làm điều này hầu như luôn sử dụng thư viện chuẩn hoặc nền tảng API để xử lý dữ liệu XML trên máy chủ. Lỗ hổng XXE phát sinh vì đặc tả XML chứa nhiều tính năng có khả năng gây nguy hiểm, và các trình phân tích cú pháp chuẩn hỗ trợ các tính năng này ngay cả khi chúng thường không được ứng dụng sử dụng.  

Các thực thể XML external là một loại thực thể XML tùy chỉnh mà các giá trị được định nghĩa của chúng được tải từ bên ngoài DTD nơi chúng được khai báo. Các thực thể external đặc biệt thú vị từ góc độ bảo mật vì chúng cho phép định nghĩa một thực thể dựa trên nội dung của đường dẫn tệp hoặc URL.  

# Khai thác lỗ hổng XXE để lấy tệp tin  
Để thực hiện cuộc tấn công chèn XXE nhằm lấy một tập tin tùy ý từ hệ thống tập tin của máy chủ, bạn cần sửa đổi XML đã gửi theo hai cách:  

* Thêm (hoặc chỉnh sửa) một phần tử `DOCTYPE` xác định thực thể bên ngoài chứa đường dẫn đến tệp.  
* Chỉnh sửa giá trị dữ liệu trong XML được trả về trong phản hồi của ứng dụng để sử dụng thực thể bên ngoài đã được định nghĩa.  

Ví dụ, giả sử một ứng dụng mua sắm kiểm tra mức tồn kho của một sản phẩm bằng cách gửi XML sau đến máy chủ:  

```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck><productId>381</productId></stockCheck>
```  

Ứng dụng không có bất kỳ biện pháp phòng vệ đặc biệt nào chống lại các cuộc tấn công XXE, vì vậy bạn có thể khai thác lỗ hổng XXE để đọc tập tin `/etc/password` bằng cách gửi đoạn mã XXE sau:  
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck><productId>&xxe;</productId></stockCheck>
```

Payload XXE này định nghĩa một thực thể external `&xxe` có giá trị là nội dung của tệp `/etc/passwd` và sử dụng thực thể đó trong giá trị `productId`. Điều này khiến phản hồi của ứng dụng bao gồm nội dung của tệp:

```
Invalid product ID: root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
...
```

## Thực hành: Khai thác lỗ hổng XXE bằng cách sử dụng các thực thể bên ngoài để truy xuất tệp  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/XXE_injection/Solution/lab1.py)

# Khai thác lỗ hổng XXE để thực hiện các cuộc tấn công SSRF 
Ngoài việc đánh cắp dữ liệu nhạy cảm, tác động chính khác của các cuộc tấn công XXE là chúng có thể được sử dụng để thực hiện giả mạo yêu cầu phía máy chủ (SSRF). Đây là một lỗ hổng tiềm tàng nghiêm trọng, trong đó ứng dụng phía máy chủ có thể bị thuyết phục thực hiện các yêu cầu HTTP đến bất kỳ URL nào mà máy chủ có thể truy cập.

Để khai thác lỗ hổng XXE nhằm thực hiện tấn công SSRF, bạn cần định nghĩa một thực thể XML bên ngoài bằng cách sử dụng URL mà bạn muốn nhắm mục tiêu, và sử dụng thực thể đã định nghĩa đó trong một giá trị dữ liệu. Nếu bạn có thể sử dụng thực thể đã định nghĩa đó trong một giá trị dữ liệu được trả về trong phản hồi của ứng dụng, thì bạn sẽ có thể xem phản hồi từ URL trong phản hồi của ứng dụng, và do đó có được sự tương tác hai chiều với hệ thống phụ trợ. Nếu không, thì bạn chỉ có thể thực hiện các cuộc tấn công SSRF mù (điều này vẫn có thể gây ra hậu quả nghiêm trọng).

Trong ví dụ XXE sau đây, thực thể bên ngoài sẽ khiến máy chủ thực hiện yêu cầu HTTP đến một hệ thống nội bộ trong cơ sở hạ tầng của tổ chức:  
```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://internal.vulnerable-website.com/"> ]>
```

## Thực hành: Khai thác lỗ hổng XXE để thực hiện các cuộc tấn công SSRF  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/XXE_injection/Solution/lab2.py)  

# Các lỗ hổng XXE mù  
Nhiều lỗ hổng XXE là lỗ hổng "mù". Điều này có nghĩa là ứng dụng không trả về giá trị của bất kỳ thực thể bên ngoài nào được định nghĩa trong phản hồi của nó, do đó việc truy xuất trực tiếp các tệp phía máy chủ là không thể.

Các lỗ hổng XXE ẩn vẫn có thể được phát hiện và khai thác, nhưng cần các kỹ thuật tiên tiến hơn. Đôi khi, bạn có thể sử dụng các kỹ thuật ngoài luồng để tìm ra các lỗ hổng và khai thác chúng để đánh cắp dữ liệu. Và đôi khi, bạn có thể kích hoạt các lỗi phân tích cú pháp XML dẫn đến việc tiết lộ dữ liệu nhạy cảm trong các thông báo lỗi.  

# Tìm kiếm bề mặt tấn công ẩn cho phép tiêm mã XXE  
Bề mặt tấn công của lỗ hổng XXE thường khá rõ ràng trong nhiều trường hợp, bởi vì lưu lượng HTTP thông thường của ứng dụng bao gồm các yêu cầu chứa dữ liệu ở định dạng XML. Trong các trường hợp khác, bề mặt tấn công ít rõ ràng hơn. Tuy nhiên, nếu bạn tìm kiếm đúng chỗ, bạn sẽ tìm thấy bề mặt tấn công XXE trong các yêu cầu không chứa bất kỳ XML nào.  

## XInclude attacks  
Một số ứng dụng nhận dữ liệu do máy khách gửi, nhúng dữ liệu đó vào một tài liệu XML ở phía máy chủ, rồi phân tích cú pháp tài liệu đó. Ví dụ, dữ liệu do máy khách gửi được đưa vào yêu cầu SOAP ở phía máy chủ, sau đó được xử lý bởi dịch vụ SOAP ở phía máy chủ.

Trong trường hợp này, bạn không thể thực hiện một cuộc tấn công XXE cổ điển, vì bạn không kiểm soát toàn bộ tài liệu XML và do đó không thể định nghĩa hoặc sửa đổi một phần tử `DOCTYPE`. Tuy nhiên, bạn có thể sử dụng `XInclude` thay thế. `XInclude` là một phần của đặc tả XML cho phép xây dựng tài liệu XML từ các tài liệu con. Bạn có thể đặt một `XInclude` cuộc tấn công vào bất kỳ giá trị dữ liệu nào trong tài liệu XML, vì vậy cuộc tấn công có thể được thực hiện trong các tình huống mà bạn chỉ kiểm soát một mục dữ liệu duy nhất được đặt trong tài liệu XML phía máy chủ.

Để thực hiện một `XInclude` cuộc tấn công, bạn cần tham chiếu đến `XInclude` không gian tên và cung cấp đường dẫn đến tệp mà bạn muốn đưa vào. Ví dụ:

```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo>
```

### Thực hành: Khai thác XInclude để truy xuất tệp  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/XXE_injection/Solution/lab3.py)  

## Tấn công XXE thông qua tải lên tập tin  
Một số ứng dụng cho phép người dùng tải lên các tệp tin, sau đó được xử lý ở phía máy chủ. Một số định dạng tệp tin phổ biến sử dụng XML hoặc chứa các thành phần con XML. Ví dụ về các định dạng dựa trên XML là các định dạng tài liệu văn phòng như DOCX và các định dạng hình ảnh như SVG.  

Ví dụ, một ứng dụng có thể cho phép người dùng tải lên hình ảnh và xử lý hoặc xác thực chúng trên máy chủ sau khi được tải lên. Ngay cả khi ứng dụng mong muốn nhận định dạng như PNG hoặc JPEG, thư viện xử lý hình ảnh đang được sử dụng có thể hỗ trợ hình ảnh SVG. Vì định dạng SVG sử dụng XML, kẻ tấn công có thể gửi một hình ảnh SVG độc hại và do đó tiếp cận được bề mặt tấn công ẩn chứa các lỗ hổng XXE.  

### Thực hành: Khai thác lỗ hổng XXE thông qua việc tải lên tập tin hình ảnh  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/XXE_injection/Solution/lab4.py)  

## Các cuộc tấn công XXE thông qua loại nội dung đã sửa đổi  
Hầu hết các yêu cầu POST sử dụng kiểu nội dung mặc định được tạo bởi các biểu mẫu HTML, chẳng hạn như `application/x-www-form-urlencoded`. Một số trang web mong đợi nhận được các yêu cầu ở định dạng này nhưng cũng chấp nhận các kiểu nội dung khác, bao gồm cả XML.  

Ví dụ, nếu một yêu cầu thông thường chứa các thông tin sau:

```http
POST /action HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 7

foo=bar
```  

Khi đó, bạn có thể gửi yêu cầu sau đây, và kết quả cũng sẽ tương tự:  
```http
POST /action HTTP/1.0
Content-Type: text/xml
Content-Length: 52

<?xml version="1.0" encoding="UTF-8"?><foo>bar</foo>
```  
Nếu ứng dụng chấp nhận các yêu cầu chứa XML trong phần thân thông báo và phân tích nội dung thân thông báo dưới dạng XML, thì bạn có thể tiếp cận bề mặt tấn công XXE ẩn bằng cách định dạng lại các yêu cầu để sử dụng định dạng XML.  

# Cách tìm và kiểm tra các lỗ hổng XXE  
Đa số các lỗ hổng XXE có thể được phát hiện nhanh chóng và đáng tin cậy bằng cách sử dụng công cụ quét lỗ hổng web của Burp Suite.

Việc kiểm tra thủ công các lỗ hổng XXE thường bao gồm:

* Kiểm tra khả năng truy xuất tập tin bằng cách định nghĩa một thực thể bên ngoài dựa trên một tập tin hệ điều hành quen thuộc và sử dụng thực thể đó trong dữ liệu được trả về trong phản hồi của ứng dụng.  
* Kiểm tra các lỗ hổng XXE ẩn bằng cách định nghĩa một thực thể bên ngoài dựa trên URL đến một hệ thống mà bạn kiểm soát, và giám sát các tương tác với hệ thống đó. Burp Collaborator là công cụ hoàn hảo cho mục đích này.  
* Kiểm tra khả năng chèn dữ liệu không phải XML do người dùng cung cấp vào tài liệu XML phía máy chủ bằng cách sử dụng tấn công XInclude để cố gắng truy xuất một tệp hệ điều hành quen thuộc.  

# Cách phòng ngừa các lỗ hổng XXE  
Hầu hết các lỗ hổng XXE đều phát sinh do thư viện phân tích cú pháp XML của ứng dụng hỗ trợ các tính năng XML tiềm ẩn nguy hiểm mà ứng dụng không cần hoặc không có ý định sử dụng. Cách dễ nhất và hiệu quả nhất để ngăn chặn các cuộc tấn công XXE là vô hiệu hóa các tính năng đó.

Thông thường, chỉ cần vô hiệu hóa việc phân giải các thực thể bên ngoài và vô hiệu hóa hỗ trợ cho XInclude là đủ. Điều này thường có thể được thực hiện thông qua các tùy chọn cấu hình hoặc bằng cách ghi đè hành vi mặc định theo chương trình. Tham khảo tài liệu của thư viện phân tích cú pháp XML hoặc API của bạn để biết chi tiết về cách vô hiệu hóa các khả năng không cần thiết.