# Reflected XSS là gì?

Tấn công kịch bản chéo trang phản xạ (hay XSS) xảy ra khi một ứng dụng nhận dữ liệu trong yêu cầu HTTP và đưa dữ liệu đó vào phản hồi ngay lập tức theo cách không an toàn.  

Giả sử một trang web có chức năng tìm kiếm nhận từ khóa tìm kiếm do người dùng cung cấp dưới dạng tham số URL:  

`https://insecure-website.com/search?term=gift`  

Ứng dụng sẽ hiển thị lại cụm từ tìm kiếm được cung cấp trong phản hồi cho URL này:  

`<p>You searched for: gift</p>`  

Giả sử ứng dụng không thực hiện bất kỳ quá trình xử lý dữ liệu nào khác, kẻ tấn công có thể xây dựng một cuộc tấn công như sau:  

`https://insecure-website.com/search?term=<script>/*+Bad+stuff+here...+*/</script>`  

URL này trả về phản hồi sau:  

`<p>You searched for: <script>/* Bad stuff here... */</script></p>`  

Nếu một người dùng khác của ứng dụng yêu cầu URL của kẻ tấn công, thì đoạn mã do kẻ tấn công cung cấp sẽ được thực thi trong trình duyệt của người dùng nạn nhân, trong ngữ cảnh phiên làm việc của họ với ứng dụng. 

## Bài thực hành: Tấn công XSS phản chiếu vào ngữ cảnh HTML mà không mã hóa bất cứ thứ gì.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Solution/lab1.py)

# Tác động của các cuộc tấn công XSS phản xạ  
Nếu kẻ tấn công có thể kiểm soát một đoạn mã được thực thi trong trình duyệt của nạn nhân, thì chúng thường có thể xâm phạm hoàn toàn người dùng đó. Trong số những việc khác, kẻ tấn công có thể:

* Thực hiện bất kỳ thao tác nào trong ứng dụng mà người dùng có thể thực hiện.
* Xem mọi thông tin mà người dùng có thể xem.
* Chỉnh sửa bất kỳ thông tin nào mà người dùng có thể chỉnh sửa.
* Khởi tạo các tương tác với người dùng ứng dụng khác, bao gồm cả các cuộc tấn công độc hại, mà thoạt nhìn sẽ có vẻ như xuất phát từ người dùng nạn nhân ban đầu.

Có nhiều cách mà kẻ tấn công có thể sử dụng để dụ người dùng nạn nhân thực hiện yêu cầu mà chúng kiểm soát, nhằm thực hiện cuộc tấn công XSS phản xạ. Những cách này bao gồm việc đặt liên kết trên trang web do kẻ tấn công kiểm soát, hoặc trên một trang web khác cho phép tạo nội dung, hoặc bằng cách gửi liên kết trong email, tweet hoặc các tin nhắn khác. Cuộc tấn công có thể nhắm trực tiếp vào một người dùng cụ thể hoặc có thể là một cuộc tấn công bừa bãi nhắm vào bất kỳ người dùng nào của ứng dụng.

Việc cần có cơ chế phân phối bên ngoài cho cuộc tấn công có nghĩa là tác động của XSS phản xạ thường ít nghiêm trọng hơn so với XSS lưu trữ, nơi một cuộc tấn công khép kín có thể được thực hiện bên trong chính ứng dụng dễ bị tổn thương.  

# Tấn công XSS phản chiếu trong các ngữ cảnh khác nhau  
Có nhiều biến thể khác nhau của tấn công kịch bản chéo trang phản xạ (reflected cross-site scripting). Vị trí của dữ liệu phản xạ trong phản hồi của ứng dụng sẽ quyết định loại mã độc cần thiết để khai thác lỗ hổng và cũng có thể ảnh hưởng đến mức độ nghiêm trọng của lỗ hổng.

Ngoài ra, nếu ứng dụng thực hiện bất kỳ quá trình xác thực hoặc xử lý nào khác trên dữ liệu đã gửi trước khi hiển thị, điều này thường sẽ ảnh hưởng đến loại mã độc XSS cần thiết.  

# Cách tìm và kiểm tra các lỗ hổng XSS phản xạ  
Đa số các lỗ hổng tấn công kịch bản chéo trang phản xạ (reflected cross-site scripting) có thể được phát hiện nhanh chóng và đáng tin cậy bằng cách sử dụng công cụ quét lỗ hổng web của Burp Suite.

Việc kiểm tra thủ công các lỗ hổng XSS phản xạ bao gồm các bước sau:  

* Kiểm tra mọi điểm truy cập. Kiểm tra riêng từng điểm truy cập để tìm dữ liệu bên trong các yêu cầu HTTP của ứng dụng. Điều này bao gồm các tham số hoặc dữ liệu khác trong chuỗi truy vấn URL và phần thân thông báo, cũng như đường dẫn tệp URL. Nó cũng bao gồm các tiêu đề HTTP, mặc dù hành vi giống XSS chỉ có thể được kích hoạt thông qua một số tiêu đề HTTP nhất định có thể không thể khai thác được trong thực tế.
* Gửi các giá trị chữ số ngẫu nhiên. Với mỗi điểm nhập liệu, hãy gửi một giá trị ngẫu nhiên duy nhất và xác định xem giá trị đó có được phản hồi hay không. Giá trị này cần được thiết kế để vượt qua hầu hết các kiểm tra xác thực đầu vào, vì vậy cần phải khá ngắn và chỉ chứa các ký tự chữ số. Nhưng nó cũng cần đủ dài để giảm thiểu khả năng trùng khớp ngẫu nhiên trong phản hồi. Một giá trị chữ số ngẫu nhiên khoảng 8 ký tự thường là lý tưởng. Bạn có thể sử dụng các payload số của Burp Intruder với các giá trị thập lục phân được tạo ngẫu nhiên để tạo ra các giá trị ngẫu nhiên phù hợp. Và bạn có thể sử dụng cài đặt payload grep của Burp Intruder để tự động gắn cờ các phản hồi chứa giá trị đã gửi.
* Xác định ngữ cảnh phản chiếu. Đối với mỗi vị trí trong phản hồi nơi giá trị ngẫu nhiên được phản chiếu, hãy xác định ngữ cảnh của nó. Điều này có thể nằm trong văn bản giữa các thẻ HTML, bên trong thuộc tính thẻ có thể được đặt trong dấu ngoặc kép, bên trong chuỗi JavaScript, v.v.
* Kiểm tra payload ứng cử viên. Dựa trên ngữ cảnh của phản hồi, hãy kiểm tra một payload XSS ứng cử viên ban đầu, payload này sẽ kích hoạt việc thực thi JavaScript nếu nó được phản ánh nguyên vẹn trong phản hồi. Cách dễ nhất để kiểm tra payload là gửi yêu cầu đến Burp Repeater , sửa đổi yêu cầu để chèn payload ứng cử viên, gửi lại yêu cầu, và sau đó xem xét phản hồi để xem payload có hoạt động hay không. Một cách làm việc hiệu quả hơn là giữ nguyên giá trị ngẫu nhiên ban đầu trong yêu cầu và đặt payload XSS ứng cử viên trước hoặc sau nó. Sau đó, đặt giá trị ngẫu nhiên đó làm thuật ngữ tìm kiếm trong chế độ xem phản hồi của Burp Repeater. Burp sẽ làm nổi bật từng vị trí mà thuật ngữ tìm kiếm xuất hiện, cho phép bạn nhanh chóng xác định vị trí phản hồi.
* Kiểm tra các payload thay thế. Nếu payload XSS ứng cử viên bị ứng dụng sửa đổi hoặc chặn hoàn toàn, bạn cần kiểm tra các payload và kỹ thuật thay thế có thể thực hiện cuộc tấn công XSS hiệu quả dựa trên ngữ cảnh phản chiếu và loại xác thực đầu vào đang được thực hiện. Để biết thêm chi tiết, hãy xem ngữ cảnh tấn công kịch bản chéo trang (cross-site scripting contexts).
* Kiểm tra cuộc tấn công trong trình duyệt. Cuối cùng, nếu bạn tìm được một payload hoạt động được trong Burp Repeater, hãy chuyển cuộc tấn công sang trình duyệt thực (bằng cách dán URL vào thanh địa chỉ hoặc sửa đổi yêu cầu trong chế độ xem chặn của Burp Proxy) và xem JavaScript được chèn có thực sự được thực thi hay không. Thông thường, tốt nhất là thực thi một số JavaScript đơn giản, ví dụ như đoạn mã `alert(document.domain)` này sẽ kích hoạt một cửa sổ bật lên hiển thị trong trình duyệt nếu cuộc tấn công thành công.