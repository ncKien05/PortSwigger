# Kiểm soát truy cập là gì?  
Kiểm soát truy cập là việc áp đặt các ràng buộc đối với người hoặc đối tượng được phép thực hiện hành động hoặc truy cập tài nguyên. Trong bối cảnh các ứng dụng web, kiểm soát truy cập phụ thuộc vào xác thực và quản lý phiên:

* Xác thực giúp người dùng nhận biết rằng họ chính là người mà họ tự xưng.
* Quản lý phiên xác định những yêu cầu HTTP tiếp theo nào đang được thực hiện bởi cùng một người dùng.
* Kiểm soát truy cập xác định xem người dùng có được phép thực hiện hành động mà họ đang cố gắng thực hiện hay không.  

Lỗi kiểm soát truy cập rất phổ biến và thường gây ra lỗ hổng bảo mật nghiêm trọng. Thiết kế và quản lý kiểm soát truy cập là một vấn đề phức tạp và năng động, đòi hỏi áp dụng các ràng buộc về kinh doanh, tổ chức và pháp lý vào việc triển khai kỹ thuật. Các quyết định thiết kế kiểm soát truy cập phải do con người đưa ra, do đó khả năng xảy ra lỗi rất cao.  

## Kiểm soát truy cập theo chiều dọc  
Kiểm soát truy cập theo chiều dọc là các cơ chế hạn chế quyền truy cập vào các chức năng nhạy cảm đối với các loại người dùng cụ thể.  

Với cơ chế kiểm soát truy cập theo chiều dọc, các loại người dùng khác nhau sẽ có quyền truy cập vào các chức năng ứng dụng khác nhau. Ví dụ, quản trị viên có thể chỉnh sửa hoặc xóa tài khoản của bất kỳ người dùng nào, trong khi người dùng thông thường không có quyền thực hiện các thao tác này. Cơ chế kiểm soát truy cập theo chiều dọc có thể là những triển khai chi tiết hơn của các mô hình bảo mật được thiết kế để thực thi các chính sách kinh doanh như phân tách nhiệm vụ và quyền hạn tối thiểu.  

## Kiểm soát truy cập ngang  
Kiểm soát truy cập theo chiều ngang là các cơ chế hạn chế quyền truy cập vào tài nguyên cho những người dùng cụ thể.  

Với cơ chế kiểm soát truy cập ngang, người dùng khác nhau có quyền truy cập vào một tập hợp con các tài nguyên cùng loại. Ví dụ, một ứng dụng ngân hàng sẽ cho phép người dùng xem giao dịch và thực hiện thanh toán từ tài khoản của chính họ, nhưng không cho phép truy cập vào tài khoản của bất kỳ người dùng nào khác.  

## Kiểm soát truy cập phụ thuộc vào ngữ cảnh  
Kiểm soát truy cập phụ thuộc vào ngữ cảnh hạn chế quyền truy cập vào các chức năng và tài nguyên dựa trên trạng thái của ứng dụng hoặc sự tương tác của người dùng với ứng dụng đó.  

Kiểm soát truy cập phụ thuộc vào ngữ cảnh ngăn người dùng thực hiện các hành động sai thứ tự. Ví dụ, một trang web bán lẻ có thể ngăn người dùng sửa đổi nội dung giỏ hàng của họ sau khi đã thanh toán.  

# Ví dụ về các lỗi kiểm soát truy cập  
Lỗ hổng kiểm soát truy cập bị phá vỡ xảy ra khi người dùng có thể truy cập tài nguyên hoặc thực hiện các hành động mà họ không được phép.  
## leo thang đặc quyền theo chiều dọc  
Nếu người dùng có thể truy cập vào các chức năng mà họ không được phép truy cập thì đó là leo thang đặc quyền theo chiều dọc. Ví dụ, nếu người dùng không có quyền quản trị có thể truy cập vào trang quản trị nơi họ có thể xóa tài khoản người dùng, thì đó là leo thang đặc quyền theo chiều dọc.  

### Chức năng không được bảo vệ  
Ở dạng cơ bản nhất, leo thang đặc quyền theo chiều dọc phát sinh khi một ứng dụng không thực thi bất kỳ biện pháp bảo vệ nào cho các chức năng nhạy cảm. Ví dụ, các chức năng quản trị có thể được liên kết từ trang chào mừng của quản trị viên nhưng không được liên kết từ trang chào mừng của người dùng. Tuy nhiên, người dùng vẫn có thể truy cập các chức năng quản trị bằng cách duyệt đến URL quản trị có liên quan.

Ví dụ, một trang web có thể lưu trữ các chức năng nhạy cảm tại URL sau:
`https://insecure-website.com/admin`  

Thông tin này có thể được truy cập bởi bất kỳ người dùng nào, không chỉ người dùng quản trị có liên kết đến chức năng này trong giao diện người dùng của họ. Trong một số trường hợp, URL quản trị có thể được tiết lộ ở những vị trí khác, chẳng hạn như trong tệp `robots.txt`:  
`https://insecure-website.com/robots.txt`  

Ngay cả khi URL không được tiết lộ ở bất kỳ đâu, kẻ tấn công vẫn có thể sử dụng danh sách từ để dò tìm vị trí của chức năng nhạy cảm bằng phương pháp vét cạn. 

#### Phòng thí nghiệm: Chức năng quản trị không được bảo vệ  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab1.py)

Trong một số trường hợp, chức năng nhạy cảm được che giấu bằng cách sử dụng URL khó đoán hơn. Đây là một ví dụ về cái gọi là "bảo mật bằng cách che giấu". Tuy nhiên, việc che giấu chức năng nhạy cảm không cung cấp khả năng kiểm soát truy cập hiệu quả vì người dùng có thể phát hiện ra URL bị che giấu bằng nhiều cách khác nhau.  

Hãy tưởng tượng một ứng dụng lưu trữ các chức năng quản trị tại URL sau:  
`https://insecure-website.com/administrator-panel-yb556`  

Điều này có thể không dễ dàng đoán được bởi kẻ tấn công. Tuy nhiên, ứng dụng vẫn có thể làm lộ URL cho người dùng. URL có thể bị tiết lộ trong mã JavaScript xây dựng giao diện người dùng dựa trên vai trò của người dùng: 

```javascript
<script>
	var isAdmin = false;
	if (isAdmin) {
		...
		var adminPanelTag = document.createElement('a');
		adminPanelTag.setAttribute('href', 'https://insecure-website.com/administrator-panel-yb556');
		adminPanelTag.innerText = 'Admin panel';
		...
	}
</script>
```

Đoạn mã này thêm một liên kết vào giao diện người dùng nếu người dùng đó là quản trị viên. Tuy nhiên, đoạn mã chứa URL này sẽ hiển thị cho tất cả người dùng bất kể vai trò của họ.  

#### Thí nghiệm: Chức năng quản trị không được bảo vệ với URL không thể dự đoán được  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab2.py)  

### Phương pháp kiểm soát truy cập dựa trên tham số  
Một số ứng dụng xác định quyền truy cập hoặc vai trò của người dùng khi đăng nhập, sau đó lưu trữ thông tin này ở vị trí mà người dùng có thể kiểm soát. Đó có thể là:

* Một trường ẩn.
* Một cookie.
* Một tham số chuỗi truy vấn được thiết lập sẵn.

Ứng dụng đưa ra quyết định kiểm soát truy cập dựa trên giá trị được gửi vào. Ví dụ:  
```
https://insecure-website.com/login/home.jsp?admin=true
https://insecure-website.com/login/home.jsp?role=1
```

Cách tiếp cận này không an toàn vì người dùng có thể sửa đổi giá trị và truy cập các chức năng mà họ không được phép, chẳng hạn như các chức năng quản trị.  

#### Thí nghiệm: Vai trò người dùng được kiểm soát bởi tham số yêu cầu  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab3.py)  

#### Thực hành: Vai trò người dùng có thể được sửa đổi trong hồ sơ người dùng.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab4.py)  

### Lỗi kiểm soát truy cập do cấu hình nền tảng không chính xác.  
Một số ứng dụng thực thi kiểm soát truy cập ở lớp nền tảng. Chúng làm điều này bằng cách hạn chế quyền truy cập vào các URL và phương thức HTTP cụ thể dựa trên vai trò của người dùng. Ví dụ, một ứng dụng có thể cấu hình quy tắc như sau:  
`DENY: POST, /admin/deleteUser, managers`  

Quy tắc này từ chối quyền truy cập vào `POST` phương thức trên URL `/admin/deleteUser` đối với người dùng thuộc nhóm quản trị. Nhiều sự cố có thể xảy ra trong tình huống này, dẫn đến việc vượt qua kiểm soát truy cập.

Một số framework ứng dụng hỗ trợ nhiều tiêu đề HTTP không chuẩn có thể được sử dụng để ghi đè URL trong yêu cầu gốc, chẳng hạn như `X-Original-URL` và `X-Rewrite-URL`. Nếu một trang web sử dụng các biện pháp kiểm soát giao diện người dùng nghiêm ngặt để hạn chế quyền truy cập dựa trên URL, nhưng ứng dụng cho phép ghi đè URL thông qua tiêu đề yêu cầu, thì có thể vượt qua các biện pháp kiểm soát truy cập bằng yêu cầu như sau:  
```
POST / HTTP/1.1
X-Original-URL: /admin/deleteUser
...
```

#### Thí nghiệm: Có thể vượt qua cơ chế kiểm soát truy cập dựa trên URL.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab5.py)  

Một kiểu tấn công khác liên quan đến phương thức HTTP được sử dụng trong yêu cầu. Các biện pháp kiểm soát phía máy chủ được mô tả trong các phần trước hạn chế quyền truy cập dựa trên URL và phương thức HTTP. Một số trang web cho phép sử dụng các phương thức yêu cầu HTTP khác nhau khi thực hiện một hành động. Nếu kẻ tấn công có thể sử dụng phương thức `GET` (hoặc một phương thức khác) để thực hiện các hành động trên một URL bị hạn chế, chúng có thể vượt qua cơ chế kiểm soát truy cập được triển khai ở lớp nền tảng.  

#### Phòng thí nghiệm: Phương pháp kiểm soát truy cập dựa trên phương pháp có thể bị vượt qua.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab6.py)  

### Lỗi kiểm soát truy cập do sự không khớp URL.  
Các trang web có thể khác nhau về mức độ nghiêm ngặt trong việc khớp đường dẫn của yêu cầu đến với một điểm cuối được xác định. Ví dụ, chúng có thể chấp nhận việc viết hoa không nhất quán, vì vậy yêu cầu tới `/ADMIN/DELETEUSER` vẫn có thể được ánh xạ đến `/admin/deleteUser` điểm cuối đó. Nếu cơ chế kiểm soát truy cập ít khoan dung hơn, nó có thể coi đây là hai điểm cuối khác nhau và do đó không thực thi các hạn chế chính xác.

Những sai lệch tương tự có thể phát sinh nếu các nhà phát triển sử dụng framework Spring đã bật `useSuffixPatternMatch`. Điều này cho phép các đường dẫn có phần mở rộng tệp tùy ý được ánh xạ tới một điểm cuối tương đương không có phần mở rộng tệp. Nói cách khác, yêu cầu tới `/admin/deleteUser.anything` vẫn sẽ khớp `/admin/deleteUser` với mẫu. Trước phiên bản Spring 5.3, tùy chọn này được bật theo mặc định.

Trên các hệ thống khác, bạn có thể gặp phải sự khác biệt trong việc liệu `/admin/deleteUser` và `/admin/deleteUser/` có được coi là các điểm cuối riêng biệt hay không. Trong trường hợp này, bạn có thể bỏ qua các kiểm soát truy cập bằng cách thêm dấu gạch chéo vào cuối đường dẫn.  

### leo thang đặc quyền theo chiều ngang
Tăng quyền truy cập theo chiều ngang xảy ra khi người dùng có thể truy cập vào tài nguyên thuộc về người dùng khác, thay vì tài nguyên cùng loại của chính họ. Ví dụ, nếu một nhân viên có thể truy cập vào hồ sơ của các nhân viên khác cũng như hồ sơ của chính mình, thì đây là tăng quyền truy cập theo chiều ngang.

Các cuộc tấn công leo thang đặc quyền theo chiều ngang có thể sử dụng các phương pháp khai thác tương tự như leo thang đặc quyền theo chiều dọc. Ví dụ, người dùng có thể truy cập trang tài khoản của chính họ bằng URL sau:  

`https://insecure-website.com/myaccount?id=123` 

Nếu kẻ tấn công thay đổi `id` giá trị tham số thành giá trị của người dùng khác, chúng có thể truy cập vào trang tài khoản của người dùng đó, cùng với dữ liệu và các chức năng liên quan.  

#### Phòng thí nghiệm: ID người dùng được kiểm soát bởi tham số yêu cầu  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab7.py)  

Trong một số ứng dụng, tham số có thể bị khai thác không có giá trị dự đoán được. Ví dụ, thay vì một số tăng dần, ứng dụng có thể sử dụng mã định danh duy nhất toàn cầu (GUID) để xác định người dùng. Điều này có thể ngăn kẻ tấn công đoán hoặc dự đoán mã định danh của người dùng khác. Tuy nhiên, các GUID thuộc về người dùng khác có thể bị tiết lộ ở những nơi khác trong ứng dụng nơi người dùng được tham chiếu, chẳng hạn như tin nhắn hoặc đánh giá của người dùng.  

#### Thí nghiệm: ID người dùng được điều khiển bởi tham số yêu cầu, với các ID người dùng không thể dự đoán được  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab8.py)  

Trong một số trường hợp, ứng dụng có thể phát hiện khi người dùng không được phép truy cập tài nguyên và trả về trang chuyển hướng về trang đăng nhập. Tuy nhiên, phản hồi chứa thông tin chuyển hướng vẫn có thể bao gồm một số dữ liệu nhạy cảm thuộc về người dùng mục tiêu, do đó cuộc tấn công vẫn thành công.  

#### Thí nghiệm: ID người dùng được kiểm soát bởi tham số yêu cầu với hiện tượng rò rỉ dữ liệu trong quá trình chuyển hướng.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab9.py)  

## leo thang đặc quyền từ ngang sang dọc
Thông thường, một cuộc tấn công leo thang đặc quyền theo chiều ngang có thể được chuyển thành leo thang đặc quyền theo chiều dọc bằng cách chiếm quyền kiểm soát người dùng có đặc quyền cao hơn. Ví dụ, leo thang theo chiều ngang có thể cho phép kẻ tấn công đặt lại hoặc lấy được mật khẩu của người dùng khác. Nếu kẻ tấn công nhắm mục tiêu vào người dùng quản trị và chiếm đoạt tài khoản của họ, thì chúng có thể giành được quyền truy cập quản trị và do đó thực hiện leo thang đặc quyền theo chiều dọc.

Kẻ tấn công có thể truy cập vào trang tài khoản của người dùng khác bằng kỹ thuật can thiệp tham số đã được mô tả ở trên đối với việc leo thang đặc quyền theo chiều ngang:  
`https://insecure-website.com/myaccount?id=456`  

Nếu người dùng mục tiêu là quản trị viên ứng dụng, thì kẻ tấn công sẽ có quyền truy cập vào trang tài khoản quản trị. Trang này có thể tiết lộ mật khẩu của quản trị viên hoặc cung cấp phương tiện để thay đổi mật khẩu, hoặc có thể cung cấp quyền truy cập trực tiếp vào các chức năng đặc quyền.  

#### Thí nghiệm: ID người dùng được kiểm soát bởi tham số yêu cầu kèm theo tiết lộ mật khẩu.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab10.py)  

## Tham chiếu đối tượng trực tiếp không an toàn  

Lỗ hổng tham chiếu trực tiếp đối tượng không an toàn (IDOR) là một loại lỗ hổng nhỏ hơn trong kiểm soát truy cập. IDOR xảy ra khi một ứng dụng sử dụng dữ liệu do người dùng cung cấp để truy cập trực tiếp vào các đối tượng và kẻ tấn công có thể sửa đổi dữ liệu đó để có được quyền truy cập trái phép. Lỗ hổng này trở nên phổ biến nhờ sự xuất hiện trong danh sách Top Ten của OWASP năm 2007. Đây chỉ là một ví dụ trong số rất nhiều lỗi triển khai có thể tạo điều kiện để vượt qua các biện pháp kiểm soát truy cập.  

#### Bài thực hành: Tham chiếu đối tượng trực tiếp không an toàn  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab11.py)  

## Các lỗ hổng kiểm soát truy cập trong quy trình nhiều bước  
Nhiều trang web triển khai các chức năng quan trọng thông qua một chuỗi các bước. Điều này thường xảy ra khi:

Cần thu thập nhiều thông tin đầu vào hoặc tùy chọn khác nhau.
Người dùng cần xem xét và xác nhận các chi tiết trước khi thực hiện thao tác.
Ví dụ, chức năng quản trị để cập nhật thông tin người dùng có thể bao gồm các bước sau:

Tải biểu mẫu chứa thông tin chi tiết của một người dùng cụ thể.
Gửi các thay đổi.
Xem lại các thay đổi và xác nhận.
Đôi khi, một trang web sẽ áp dụng các biện pháp kiểm soát truy cập nghiêm ngặt đối với một số bước, nhưng lại bỏ qua những bước khác. Hãy tưởng tượng một trang web mà các biện pháp kiểm soát truy cập được áp dụng chính xác cho bước thứ nhất và thứ hai, nhưng không áp dụng cho bước thứ ba. Trang web cho rằng người dùng chỉ có thể đến bước 3 nếu họ đã hoàn thành hai bước đầu tiên, vốn được kiểm soát đúng cách. Kẻ tấn công có thể truy cập trái phép vào chức năng bằng cách bỏ qua hai bước đầu tiên và trực tiếp gửi yêu cầu cho bước thứ ba với các tham số cần thiết.  

#### Thí nghiệm: Quy trình nhiều bước, không có kiểm soát truy cập ở một bước nào đó.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab12.py)  

## Kiểm soát truy cập dựa trên nguồn giới thiệu  
Một số trang web dựa vào thông tin `Referer` tiêu đề được gửi trong yêu cầu HTTP để thiết lập quyền truy cập. Trình duyệt có thể thêm tiêu đề `Referer` vào các yêu cầu để chỉ ra trang nào đã khởi tạo yêu cầu.

Ví dụ, một ứng dụng thực thi kiểm soát truy cập mạnh mẽ đối với trang quản trị chính tại `/admin`, nhưng đối với các trang con như `/admin/deleteUser` chỉ kiểm tra tiêu đề `Referer`. Nếu tiêu đề `Referer` chứa URL chính `/admin`, thì yêu cầu được cho phép.

Trong trường hợp này, kẻ tấn công có thể hoàn toàn kiểm soát phần tiêu đề `Referer`. Điều này có nghĩa là chúng có thể giả mạo các yêu cầu trực tiếp đến các trang con nhạy cảm bằng cách cung cấp tiêu đề `Referer` cần thiết và giành quyền truy cập trái phép.   

#### Phòng thí nghiệm: Kiểm soát truy cập dựa trên người giới thiệu  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Access_Control_Vulnerabilities/Solution/lab13.py)  

## Kiểm soát truy cập dựa trên vị trí  
Một số trang web áp dụng các biện pháp kiểm soát truy cập dựa trên vị trí địa lý của người dùng. Điều này có thể áp dụng, ví dụ, cho các ứng dụng ngân hàng hoặc dịch vụ truyền thông nơi luật pháp tiểu bang hoặc các hạn chế kinh doanh được áp dụng. Các biện pháp kiểm soát truy cập này thường có thể bị vượt qua bằng cách sử dụng máy chủ proxy web, VPN hoặc thao tác các cơ chế định vị địa lý phía máy khách.  

# Cách ngăn ngừa các lỗ hổng kiểm soát truy cập  

Các lỗ hổng bảo mật trong kiểm soát truy cập có thể được ngăn chặn bằng cách áp dụng phương pháp phòng thủ nhiều lớp và tuân thủ các nguyên tắc sau:

* Không bao giờ nên chỉ dựa vào việc che giấu mã nguồn để kiểm soát quyền truy cập.
* Trừ khi tài nguyên đó được thiết kế để công khai, hãy từ chối quyền truy cập theo mặc định.
* Nếu có thể, hãy sử dụng một cơ chế duy nhất áp dụng cho toàn bộ ứng dụng để thực thi kiểm soát truy cập.
* Ở cấp độ mã nguồn, hãy bắt buộc các nhà phát triển phải khai báo quyền truy cập được cho phép đối với từng tài nguyên và từ chối quyền truy cập theo mặc định.
* Kiểm tra và thử nghiệm kỹ lưỡng các biện pháp kiểm soát truy cập để đảm bảo chúng hoạt động đúng như thiết kế. 





