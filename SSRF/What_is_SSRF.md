# Server-side request forgery (SSRF)
Trong phần này, chúng tôi sẽ giải thích tấn công giả mạo yêu cầu phía máy chủ (SSRF) là gì và mô tả một số ví dụ phổ biến. Chúng tôi cũng sẽ hướng dẫn bạn cách tìm và khai thác các lỗ hổng SSRF.  
# SSRF là gì?  
Tấn công giả mạo yêu cầu phía máy chủ (Server-side request forgery) là một lỗ hổng bảo mật web cho phép kẻ tấn công khiến ứng dụng phía máy chủ thực hiện các yêu cầu đến một vị trí không mong muốn.  

Trong một cuộc tấn công SSRF điển hình, kẻ tấn công có thể khiến máy chủ kết nối với các dịch vụ nội bộ trong cơ sở hạ tầng của tổ chức. Trong các trường hợp khác, chúng có thể buộc máy chủ kết nối với các hệ thống bên ngoài tùy ý. Điều này có thể làm rò rỉ dữ liệu nhạy cảm, chẳng hạn như thông tin xác thực.  

# Tấn công SSRF gây ra những hậu quả gì?  
Một cuộc tấn công SSRF thành công thường có thể dẫn đến các hành động trái phép hoặc truy cập dữ liệu trong tổ chức. Điều này có thể xảy ra trong ứng dụng dễ bị tổn thương hoặc trên các hệ thống phụ trợ khác mà ứng dụng có thể giao tiếp. Trong một số trường hợp, lỗ hổng SSRF có thể cho phép kẻ tấn công thực hiện các lệnh tùy ý.  

Lỗ hổng SSRF gây ra kết nối đến các hệ thống bên ngoài của bên thứ ba có thể dẫn đến các cuộc tấn công độc hại tiếp theo. Những cuộc tấn công này có thể xuất phát từ tổ chức đang lưu trữ ứng dụng dễ bị tổn thương.  
# Các cuộc tấn công SSRF phổ biến  
Các cuộc tấn công SSRF thường khai thác các mối quan hệ tin cậy để leo thang cuộc tấn công từ ứng dụng dễ bị tổn thương và thực hiện các hành động trái phép. Các mối quan hệ tin cậy này có thể tồn tại liên quan đến máy chủ, hoặc liên quan đến các hệ thống phụ trợ khác trong cùng một tổ chức.  
## Các cuộc tấn công SSRF vào máy chủ  
Trong một cuộc tấn công SSRF nhằm vào máy chủ, kẻ tấn công khiến ứng dụng thực hiện yêu cầu HTTP trở lại máy chủ đang lưu trữ ứng dụng đó, thông qua giao diện mạng loopback của nó. Điều này thường liên quan đến việc cung cấp một URL với tên máy chủ như `127.0.0.1` (một địa chỉ IP dành riêng trỏ đến bộ điều hợp loopback) hoặc `localhost` (một tên thường được sử dụng cho cùng một bộ điều hợp).  

Ví dụ, hãy tưởng tượng một ứng dụng mua sắm cho phép người dùng xem một mặt hàng có còn hàng tại một cửa hàng cụ thể hay không. Để cung cấp thông tin tồn kho, ứng dụng phải truy vấn nhiều API REST phía máy chủ. Ứng dụng thực hiện điều này bằng cách truyền URL đến điểm cuối API phía máy chủ có liên quan thông qua yêu cầu HTTP phía giao diện người dùng. Khi người dùng xem trạng thái tồn kho của một mặt hàng, trình duyệt của họ sẽ thực hiện yêu cầu sau:  

```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://stock.weliketoshop.net:8080/product/stock/check%3FproductId%3D6%26storeId%3D1
```  

Điều này khiến máy chủ gửi yêu cầu đến URL được chỉ định, truy xuất trạng thái hàng tồn kho và trả về thông tin này cho người dùng.  

Trong ví dụ này, kẻ tấn công có thể sửa đổi yêu cầu để chỉ định một URL cục bộ trên máy chủ:  
```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://localhost/admin
```

Máy chủ sẽ lấy nội dung của `/admin` URL và trả về cho người dùng.  

Kẻ tấn công có thể truy cập `/admin` URL, nhưng chức năng quản trị thường chỉ dành cho người dùng đã được xác thực. Điều này có nghĩa là kẻ tấn công sẽ không thấy bất cứ điều gì đáng quan tâm. Tuy nhiên, nếu yêu cầu đến `/admin` URL này xuất phát từ máy tính cục bộ, các biện pháp kiểm soát truy cập thông thường sẽ bị bỏ qua. Ứng dụng sẽ cấp quyền truy cập đầy đủ vào chức năng quản trị, vì yêu cầu dường như xuất phát từ một vị trí đáng tin cậy.  

### Bài thực hành: Tấn công SSRF cơ bản vào máy chủ cục bộ  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/SSRF/Solution/lab1.py)

Tại sao các ứng dụng lại hoạt động theo cách này và ngầm tin tưởng các yêu cầu đến từ máy cục bộ? Điều này có thể phát sinh vì nhiều lý do:

* Việc kiểm tra quyền truy cập có thể được thực hiện trong một thành phần khác nằm phía trước máy chủ ứng dụng. Khi kết nối được thiết lập trở lại máy chủ, quá trình kiểm tra này sẽ bị bỏ qua.  
* Để phục vụ mục đích khôi phục sau sự cố, ứng dụng có thể cho phép truy cập quản trị mà không cần đăng nhập, cho bất kỳ người dùng nào truy cập từ máy cục bộ. Điều này cung cấp một cách để quản trị viên khôi phục hệ thống nếu họ mất thông tin đăng nhập. Điều này giả định rằng chỉ người dùng hoàn toàn đáng tin cậy mới truy cập trực tiếp từ máy chủ.  
* Giao diện quản trị có thể lắng nghe trên một số cổng khác với ứng dụng chính và người dùng có thể không truy cập trực tiếp được.  

Các mối quan hệ tin cậy kiểu này, trong đó các yêu cầu xuất phát từ máy cục bộ được xử lý khác với các yêu cầu thông thường, thường biến SSRF thành một lỗ hổng nghiêm trọng.  

## Các cuộc tấn công SSRF nhằm vào các hệ thống phụ trợ khác  
Trong một số trường hợp, máy chủ ứng dụng có thể tương tác với các hệ thống phụ trợ mà người dùng không thể truy cập trực tiếp. Các hệ thống này thường có địa chỉ IP riêng không thể định tuyến. Các hệ thống phụ trợ thường được bảo vệ bởi cấu trúc mạng, do đó chúng thường có mức độ bảo mật yếu hơn. Trong nhiều trường hợp, các hệ thống phụ trợ nội bộ chứa các chức năng nhạy cảm mà bất kỳ ai có thể tương tác với các hệ thống đó đều có thể truy cập mà không cần xác thực.

Trong ví dụ trước, hãy tưởng tượng có một giao diện quản trị tại URL máy chủ `https://192.168.0.68/admin`. Kẻ tấn công có thể gửi yêu cầu sau để khai thác lỗ hổng SSRF và truy cập vào giao diện quản trị:  

```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://192.168.0.68/admin
```

### Thực hành: Tấn công SSRF cơ bản vào một hệ thống máy chủ khác.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/SSRF/Solution/lab2.py)

# Vượt qua các biện pháp phòng thủ SSRF phổ biến  
Thường thấy các ứng dụng chứa hành vi SSRF cùng với các biện pháp phòng vệ nhằm ngăn chặn việc khai thác độc hại. Tuy nhiên, các biện pháp phòng vệ này thường có thể bị vượt qua.  
## SSRF với bộ lọc đầu vào dựa trên danh sách đen  
Một số ứng dụng chặn đầu vào chứa tên máy chủ như `127.0.0.1` và `localhost`, hoặc các URL nhạy cảm như `/admin`. Trong trường hợp này, bạn thường có thể vượt qua bộ lọc bằng các kỹ thuật sau:

* Hãy sử dụng cách biểu diễn IP thay thế cho `127.0.0.1`, chẳng hạn như `2130706433`, `017700000001`, hoặc `127.1`.  
* Hãy đăng ký tên miền riêng của bạn có độ phân giải thành `127.0.0.1`. Bạn có thể sử dụng `spoofed.burpcollaborator.net` cho mục đích này.  
* Che giấu các chuỗi bị chặn bằng cách sử dụng mã hóa URL hoặc biến thể chữ hoa chữ thường.  
* Hãy cung cấp một URL mà bạn kiểm soát, URL này sẽ chuyển hướng đến URL đích. Hãy thử sử dụng các mã chuyển hướng khác nhau, cũng như các giao thức khác nhau cho URL đích. Ví dụ, việc chuyển đổi từ URL này `http` sang `https` URL khác trong quá trình chuyển hướng đã được chứng minh là có thể vượt qua một số bộ lọc chống SSRF.    

### Thí nghiệm: SSRF với bộ lọc đầu vào dựa trên danh sách đen  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/SSRF/Solution/lab3.py)

## SSRF với bộ lọc đầu vào dựa trên danh sách trắng  
Một số ứng dụng chỉ cho phép nhập các giá trị khớp với danh sách trắng các giá trị được cho phép. Bộ lọc có thể tìm kiếm sự trùng khớp ở đầu hoặc bên trong chuỗi nhập liệu. Bạn có thể vượt qua bộ lọc này bằng cách khai thác các điểm không nhất quán trong quá trình phân tích cú pháp URL.  

Đặc tả URL chứa một số tính năng có thể bị bỏ qua khi URL thực hiện phân tích cú pháp và xác thực tùy ý bằng phương pháp này:  

* Bạn có thể nhúng thông tin xác thực vào URL trước tên máy chủ bằng cách sử dụng @ ký tự. Ví dụ:

    `https://expected-host:fakepassword@evil-host`  

* Bạn có thể sử dụng # ký tự này để chỉ định một phần của URL. Ví dụ:

    `https://evil-host#expected-host`  

* Bạn có thể tận dụng hệ thống phân cấp đặt tên DNS để đưa thông tin cần thiết vào một tên DNS đủ điều kiện mà bạn kiểm soát. Ví dụ:

    `https://expected-host.evil-host`  

* Bạn có thể mã hóa URL các ký tự để gây nhầm lẫn cho mã phân tích cú pháp URL. Điều này đặc biệt hữu ích nếu mã thực hiện bộ lọc xử lý các ký tự được mã hóa URL khác với mã thực hiện yêu cầu HTTP ở phía máy chủ. Bạn cũng có thể thử mã hóa kép các ký tự; một số máy chủ giải mã URL đệ quy đầu vào mà chúng nhận được, điều này có thể dẫn đến những sai lệch hơn nữa.  
* Bạn có thể kết hợp các kỹ thuật này với nhau.  

### Thí nghiệm: SSRF với bộ lọc đầu vào dựa trên danh sách trắng  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/SSRF/Solution/lab4.py)  

## Vượt qua bộ lọc SSRF thông qua chuyển hướng mở  
Đôi khi, có thể vượt qua các biện pháp phòng thủ dựa trên bộ lọc bằng cách khai thác lỗ hổng chuyển hướng đang mở.

Trong ví dụ trước, hãy tưởng tượng URL do người dùng gửi được kiểm tra nghiêm ngặt để ngăn chặn việc khai thác độc hại hành vi SSRF. Tuy nhiên, ứng dụng có các URL được cho phép lại chứa một lỗ hổng chuyển hướng đang mở. Nếu API được sử dụng để thực hiện yêu cầu HTTP phía máy chủ hỗ trợ chuyển hướng, bạn có thể tạo một URL thỏa mãn bộ lọc và dẫn đến yêu cầu được chuyển hướng đến mục tiêu máy chủ mong muốn.

Ví dụ, ứng dụng này chứa một lỗ hổng chuyển hướng mở trong đó URL sau:  

`/product/nextProduct?currentProductId=6&path=http://evil-user.net`  

Trả về một liên kết chuyển hướng đến:  
`http://evil-user.net`  
Bạn có thể tận dụng lỗ hổng chuyển hướng mở để vượt qua bộ lọc URL và khai thác lỗ hổng SSRF như sau:  
```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://weliketoshop.net/product/nextProduct?currentProductId=6&path=http://192.168.0.68/admin
```

Lỗ hổng SSRF này hoạt động vì ứng dụng trước tiên xác thực xem `stockAPI` URL được cung cấp có nằm trên một miền được cho phép hay không, và đúng là như vậy. Sau đó, ứng dụng yêu cầu URL được cung cấp, điều này kích hoạt chuyển hướng mở. Nó theo dõi đường dẫn chuyển hướng và thực hiện yêu cầu đến URL nội bộ do kẻ tấn công lựa chọn.  

### Thực hành: Tấn công SSRF vượt qua bộ lọc thông qua lỗ hổng chuyển hướng mở  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/SSRF/Solution/lab5.py)  

# Các lỗ hổng SSRF ẩn  

Lỗ hổng SSRF mù xảy ra khi bạn có thể khiến một ứng dụng gửi yêu cầu HTTP đến máy chủ phụ trợ tới một URL được cung cấp, nhưng phản hồi từ yêu cầu máy chủ phụ trợ đó không được trả về trong phản hồi phía giao diện người dùng của ứng dụng.

Lỗ hổng Blind SSRF khó khai thác hơn nhưng đôi khi dẫn đến việc thực thi mã từ xa hoàn toàn trên máy chủ hoặc các thành phần phụ trợ khác.  

# Tìm kiếm bề mặt tấn công tiềm ẩn cho các lỗ hổng SSRF  

Nhiều lỗ hổng giả mạo yêu cầu phía máy chủ (SSRF) rất dễ phát hiện vì lưu lượng truy cập thông thường của ứng dụng bao gồm các tham số yêu cầu chứa URL đầy đủ. Các ví dụ khác về SSRF khó tìm hơn.  

## URL một phần trong yêu cầu  
Đôi khi, một ứng dụng chỉ đặt tên máy chủ hoặc một phần đường dẫn URL vào các tham số yêu cầu. Giá trị được gửi sau đó được kết hợp ở phía máy chủ vào một URL hoàn chỉnh được yêu cầu. Nếu giá trị đó dễ dàng được nhận dạng là tên máy chủ hoặc đường dẫn URL, thì bề mặt tấn công tiềm tàng có thể khá rõ ràng. Tuy nhiên, khả năng khai thác lỗ hổng SSRF toàn diện có thể bị hạn chế vì bạn không kiểm soát toàn bộ URL được yêu cầu.  
## URL trong các định dạng dữ liệu  
Một số ứng dụng truyền dữ liệu ở các định dạng có đặc tả cho phép bao gồm các URL mà trình phân tích dữ liệu có thể yêu cầu cho định dạng đó. Một ví dụ rõ ràng về điều này là định dạng dữ liệu XML, được sử dụng rộng rãi trong các ứng dụng web để truyền dữ liệu có cấu trúc từ máy khách đến máy chủ. Khi một ứng dụng chấp nhận dữ liệu ở định dạng XML và phân tích nó, nó có thể dễ bị tấn công XXE. Nó cũng có thể dễ bị tấn công SSRF thông qua XXE. Chúng ta sẽ đề cập chi tiết hơn về vấn đề này khi xem xét các lỗ hổng tấn công XXE.  

## SSRF thông qua tiêu đề Referer  
Một số ứng dụng sử dụng phần mềm phân tích phía máy chủ để theo dõi khách truy cập. Phần mềm này thường ghi lại tiêu đề Referer trong các yêu cầu, để có thể theo dõi các liên kết đến. Thông thường, phần mềm phân tích sẽ truy cập bất kỳ URL bên thứ ba nào xuất hiện trong tiêu đề Referer. Điều này thường được thực hiện để phân tích nội dung của các trang web giới thiệu, bao gồm cả văn bản neo được sử dụng trong các liên kết đến. Do đó, tiêu đề Referer thường là một bề mặt tấn công hữu ích cho các lỗ hổng SSRF.  


