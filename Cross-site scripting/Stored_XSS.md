# Tấn công kịch bản chéo trang lưu trữ (Stored Cross-Site Scripting)  
Tấn công kịch bản chéo trang lưu trữ (còn được gọi là XSS bậc hai hoặc XSS dai dẳng) xảy ra khi một ứng dụng nhận dữ liệu từ một nguồn không đáng tin cậy và đưa dữ liệu đó vào các phản hồi HTTP sau đó theo cách không an toàn.

Giả sử một trang web cho phép người dùng gửi bình luận về các bài đăng trên blog, và những bình luận này sẽ được hiển thị cho những người dùng khác. Người dùng gửi bình luận bằng cách sử dụng yêu cầu HTTP như sau:  

```http
POST /post/comment HTTP/1.1
Host: vulnerable-website.com
Content-Length: 100

postId=3&comment=This+post+was+extremely+helpful.&name=Carlos+Montoya&email=carlos%40normal-user.net
```  

Sau khi bình luận này được gửi đi, bất kỳ người dùng nào truy cập bài đăng trên blog sẽ nhận được thông báo sau trong phản hồi của ứng dụng:  

`<p>This post was extremely helpful.</p>`  

Giả sử ứng dụng không thực hiện bất kỳ quá trình xử lý dữ liệu nào khác, kẻ tấn công có thể gửi một bình luận độc hại như sau:  

`<script>/* Bad stuff here... */</script>`  

Trong yêu cầu của kẻ tấn công, bình luận này sẽ được mã hóa URL như sau:  

`comment=%3Cscript%3E%2F*%2BBad%2Bstuff%2Bhere...%2B*%2F%3C%2Fscript%3E`  

Bất kỳ người dùng nào truy cập bài đăng trên blog giờ đây sẽ nhận được thông báo sau trong phản hồi của ứng dụng:  

`<p><script>/* Bad stuff here... */</script></p>`  

Đoạn mã do kẻ tấn công cung cấp sau đó sẽ được thực thi trong trình duyệt của người dùng nạn nhân, trong ngữ cảnh phiên làm việc của họ với ứng dụng.  

## Bài thực hành: Chèn mã XSS vào ngữ cảnh HTML mà không mã hóa bất cứ thứ gì.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/solution/lab2.py)  

# Tác động của các cuộc tấn công XSS lưu trữ  
Nếu kẻ tấn công có thể kiểm soát một đoạn mã được thực thi trong trình duyệt của nạn nhân, thì chúng thường có thể xâm phạm hoàn toàn người dùng đó. Kẻ tấn công có thể thực hiện bất kỳ hành động nào áp dụng cho tác động của lỗ hổng XSS phản xạ .

Về khả năng khai thác, sự khác biệt chính giữa XSS phản xạ và XSS lưu trữ là lỗ hổng XSS lưu trữ cho phép các cuộc tấn công tự chứa trong chính ứng dụng. Kẻ tấn công không cần phải tìm cách bên ngoài để khiến người dùng khác thực hiện một yêu cầu cụ thể chứa mã khai thác của chúng. Thay vào đó, kẻ tấn công đặt mã khai thác vào chính ứng dụng và chỉ cần chờ người dùng gặp phải nó.

Tính chất khép kín của các lỗ hổng kịch bản chéo trang (XSS) được lưu trữ đặc biệt quan trọng trong các trường hợp lỗ hổng XSS chỉ ảnh hưởng đến người dùng hiện đang đăng nhập vào ứng dụng. Nếu XSS được phản ánh, thì cuộc tấn công phải được thực hiện vào thời điểm ngẫu nhiên: người dùng bị dụ dỗ thực hiện yêu cầu của kẻ tấn công vào thời điểm họ không đăng nhập sẽ không bị ảnh hưởng. Ngược lại, nếu XSS được lưu trữ, thì người dùng chắc chắn sẽ đang đăng nhập vào thời điểm họ gặp phải lỗ hổng.  

# Lỗ hổng XSS lưu trữ trong các ngữ cảnh khác nhau  
Có nhiều biến thể khác nhau của tấn công kịch bản chéo trang (CSSS) được lưu trữ. Vị trí của dữ liệu được lưu trữ trong phản hồi của ứng dụng sẽ quyết định loại mã độc cần thiết để khai thác lỗ hổng và cũng có thể ảnh hưởng đến mức độ nghiêm trọng của lỗ hổng.

Ngoài ra, nếu ứng dụng thực hiện bất kỳ quá trình xác thực hoặc xử lý nào khác trên dữ liệu trước khi lưu trữ, hoặc tại thời điểm dữ liệu đã lưu trữ được tích hợp vào phản hồi, điều này thường sẽ ảnh hưởng đến loại mã độc XSS cần thiết.  

# Cách tìm và kiểm tra các lỗ hổng XSS lưu trữ  
Nhiều lỗ hổng XSS ẩn có thể được tìm thấy bằng cách sử dụng công cụ quét lỗ hổng web của Burp Suite.

Việc kiểm tra thủ công các lỗ hổng XSS lưu trữ có thể rất khó khăn. Bạn cần kiểm tra tất cả các "điểm vào" có liên quan mà qua đó dữ liệu do kẻ tấn công kiểm soát có thể đi vào quá trình xử lý của ứng dụng, và tất cả các "điểm ra" mà dữ liệu đó có thể xuất hiện trong phản hồi của ứng dụng.

Các điểm tiếp nhận thông tin trong quá trình xử lý đơn đăng ký bao gồm:

* Các tham số hoặc dữ liệu khác nằm trong chuỗi truy vấn URL và nội dung thông báo.
* Đường dẫn URL của tệp.
* Các tiêu đề yêu cầu HTTP có thể không bị khai thác liên quan đến XSS phản xạ.
* Bất kỳ tuyến đường nào nằm ngoài luồng mà kẻ tấn công có thể sử dụng để đưa dữ liệu vào ứng dụng. Các tuyến đường tồn tại hoàn toàn phụ thuộc vào chức năng được ứng dụng triển khai: một ứng dụng webmail sẽ xử lý dữ liệu nhận được trong email; một ứng dụng hiển thị nguồn cấp dữ liệu Twitter có thể xử lý dữ liệu có trong các tweet của bên thứ ba; và một trình tổng hợp tin tức sẽ bao gồm dữ liệu có nguồn gốc từ các trang web khác.  

Các điểm thoát cho các cuộc tấn công XSS lưu trữ là tất cả các phản hồi HTTP có thể được trả về cho bất kỳ người dùng ứng dụng nào trong bất kỳ tình huống nào.

Bước đầu tiên trong việc kiểm tra các lỗ hổng XSS lưu trữ là xác định các liên kết giữa điểm vào và điểm ra, trong đó dữ liệu được gửi đến điểm vào được phát ra từ điểm ra. Lý do khiến điều này có thể khó khăn là vì:

* Về nguyên tắc, dữ liệu được gửi đến bất kỳ điểm nhập nào đều có thể được xuất ra từ bất kỳ điểm xuất nào. Ví dụ, tên hiển thị do người dùng cung cấp có thể xuất hiện trong nhật ký kiểm toán ẩn mà chỉ một số người dùng ứng dụng mới nhìn thấy.
* Dữ liệu hiện đang được ứng dụng lưu trữ thường dễ bị ghi đè do các thao tác khác được thực hiện trong ứng dụng. Ví dụ, chức năng tìm kiếm có thể hiển thị danh sách các tìm kiếm gần đây, và danh sách này sẽ nhanh chóng bị thay thế khi người dùng thực hiện các tìm kiếm khác.  

Để xác định một cách toàn diện các liên kết giữa điểm vào và điểm ra, cần phải kiểm tra từng hoán vị riêng biệt, nhập một giá trị cụ thể vào điểm vào, điều hướng trực tiếp đến điểm ra và xác định xem giá trị đó có xuất hiện ở đó hay không. Tuy nhiên, cách tiếp cận này không thực tế đối với một ứng dụng có nhiều hơn một vài trang.

Thay vào đó, một cách tiếp cận thực tế hơn là làm việc một cách có hệ thống thông qua các điểm nhập dữ liệu, gửi một giá trị cụ thể vào từng điểm và theo dõi phản hồi của ứng dụng để phát hiện các trường hợp giá trị đã gửi xuất hiện. Có thể đặc biệt chú ý đến các chức năng ứng dụng có liên quan, chẳng hạn như bình luận trên bài đăng blog. Khi giá trị đã gửi được quan sát thấy trong phản hồi, bạn cần xác định xem dữ liệu đó có thực sự được lưu trữ trong các yêu cầu khác nhau hay chỉ đơn giản là được phản ánh trong phản hồi tức thì.

Khi bạn đã xác định được các liên kết giữa điểm vào và điểm ra trong quá trình xử lý ứng dụng, mỗi liên kết cần được kiểm tra cụ thể để phát hiện xem có lỗ hổng XSS lưu trữ hay không. Điều này bao gồm việc xác định ngữ cảnh trong phản hồi nơi dữ liệu được lưu trữ xuất hiện và kiểm tra các payload XSS ứng cử viên phù hợp với ngữ cảnh đó. Ở giai đoạn này, phương pháp kiểm tra nhìn chung tương tự như phương pháp tìm kiếm lỗ hổng XSS phản xạ .