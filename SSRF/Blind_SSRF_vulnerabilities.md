# Blind SSRF vulnerabilities  

Trong phần này, chúng ta sẽ giải thích tấn công giả mạo yêu cầu phía máy chủ (SSRF) mù là gì, mô tả một số ví dụ SSRF mù phổ biến và giải thích cách tìm và khai thác các lỗ hổng SSRF mù.  

# SSRF mù là gì?  
Lỗ hổng SSRF mù phát sinh khi một ứng dụng có thể bị tác động để gửi yêu cầu HTTP đến máy chủ phụ trợ tới một URL được cung cấp, nhưng phản hồi từ yêu cầu máy chủ phụ trợ đó không được trả về trong phản hồi phía giao diện người dùng của ứng dụng.  
# Các lỗ hổng SSRF ẩn gây ra những ảnh hưởng gì?  
Tác động của các lỗ hổng SSRF mù thường thấp hơn so với các lỗ hổng SSRF đầy đủ thông tin do tính chất một chiều của chúng. Chúng không thể dễ dàng bị khai thác để lấy dữ liệu nhạy cảm từ các hệ thống máy chủ, mặc dù trong một số trường hợp, chúng có thể bị khai thác để thực hiện thực thi mã từ xa hoàn toàn.  
# Cách tìm và khai thác các lỗ hổng SSRF ẩn  
Cách đáng tin cậy nhất để phát hiện các lỗ hổng SSRF ẩn là sử dụng các kỹ thuật ngoài băng tần (OAST). Điều này bao gồm việc cố gắng kích hoạt một yêu cầu HTTP đến một hệ thống bên ngoài mà bạn kiểm soát, và giám sát các tương tác mạng với hệ thống đó.

Cách dễ nhất và hiệu quả nhất để sử dụng các kỹ thuật tấn công ngoài băng tần là sử dụng Burp Collaborator . Bạn có thể sử dụng Burp Collaborator để tạo ra các tên miền duy nhất, gửi chúng trong các gói dữ liệu đến ứng dụng và theo dõi bất kỳ tương tác nào với các tên miền đó. Nếu phát hiện thấy yêu cầu HTTP đến từ ứng dụng, thì ứng dụng đó dễ bị tấn công SSRF.  

**Ghi chú**
Khi kiểm tra các lỗ hổng SSRF, việc quan sát thấy quá trình tra cứu DNS cho tên miền Collaborator được cung cấp, nhưng không có yêu cầu HTTP nào tiếp theo là điều khá phổ biến. Điều này thường xảy ra vì ứng dụng đã cố gắng thực hiện yêu cầu HTTP đến tên miền đó, dẫn đến quá trình tra cứu DNS ban đầu, nhưng yêu cầu HTTP thực tế đã bị chặn bởi bộ lọc ở cấp độ mạng. Việc cho phép lưu lượng DNS đi ra ngoài là khá phổ biến, vì điều này cần thiết cho rất nhiều mục đích, nhưng lại chặn các kết nối HTTP đến các đích không mong muốn.  

## Thí nghiệm: SSRF mù với phát hiện ngoài băng tần  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/SSRF/Solution/lab6.py)

Việc chỉ đơn thuần xác định một lỗ hổng SSRF ẩn có thể kích hoạt các yêu cầu HTTP ngoài băng tần không tự nó đã cung cấp con đường dẫn đến khả năng khai thác. Vì bạn không thể xem phản hồi từ yêu cầu phía máy chủ, nên hành vi này không thể được sử dụng để khám phá nội dung trên các hệ thống mà máy chủ ứng dụng có thể truy cập. Tuy nhiên, nó vẫn có thể được tận dụng để dò tìm các lỗ hổng khác trên chính máy chủ hoặc trên các hệ thống máy chủ khác. Bạn có thể quét mù không gian địa chỉ IP nội bộ, gửi các payload được thiết kế để phát hiện các lỗ hổng đã biết. Nếu các payload đó cũng sử dụng các kỹ thuật ngoài băng tần ẩn, thì bạn có thể phát hiện ra một lỗ hổng nghiêm trọng trên một máy chủ nội bộ chưa được vá lỗi.  

## Thí nghiệm: Sử dụng SSRF mù với khai thác Shellshock
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/SSRF/Solution/lab7.py)

Một cách khác để khai thác các lỗ hổng SSRF ẩn là khiến ứng dụng kết nối với một hệ thống nằm dưới sự kiểm soát của kẻ tấn công, và trả về các phản hồi độc hại cho máy khách HTTP thực hiện kết nối đó. Nếu bạn có thể khai thác một lỗ hổng nghiêm trọng phía máy khách trong triển khai HTTP của máy chủ, bạn có thể đạt được khả năng thực thi mã từ xa trong cơ sở hạ tầng ứng dụng.  
