# Information disclosure vulnerabilities  
Trong phần này, chúng ta sẽ giải thích những kiến ​​thức cơ bản về các lỗ hổng tiết lộ thông tin và mô tả cách bạn có thể tìm và khai thác chúng. Chúng ta cũng sẽ đưa ra một số hướng dẫn về cách bạn có thể ngăn chặn các lỗ hổng tiết lộ thông tin trên trang web của mình.  

Học cách tìm kiếm và khai thác lỗ hổng bảo mật là một kỹ năng thiết yếu đối với bất kỳ người kiểm thử nào. Bạn có thể sẽ thường xuyên gặp phải tình huống này và một khi bạn biết cách khai thác nó hiệu quả, nó có thể giúp bạn nâng cao hiệu quả kiểm thử và tìm ra thêm nhiều lỗi nghiêm trọng khác.  

# What is information disclosure?

Việc tiết lộ thông tin, hay còn gọi là rò rỉ thông tin, xảy ra khi một trang web vô tình để lộ thông tin nhạy cảm cho người dùng. Tùy thuộc vào ngữ cảnh, các trang web có thể làm rò rỉ nhiều loại thông tin khác nhau cho kẻ tấn công tiềm năng, bao gồm:  
* Dữ liệu về những người dùng khác, chẳng hạn như tên người dùng hoặc thông tin tài chính.  
* Dữ liệu thương mại hoặc kinh doanh nhạy cảm  
* Thông tin kỹ thuật chi tiết về trang web và cơ sở hạ tầng của nó.  

Nguy hiểm của việc rò rỉ dữ liệu nhạy cảm của người dùng hoặc dữ liệu kinh doanh là khá rõ ràng, nhưng việc tiết lộ thông tin kỹ thuật đôi khi cũng nghiêm trọng không kém. Mặc dù một số thông tin này sẽ có ích lợi hạn chế, nhưng nó có thể là điểm khởi đầu để phát hiện thêm một bề mặt tấn công khác, có thể chứa các lỗ hổng bảo mật thú vị khác. Kiến thức mà bạn thu thập được thậm chí có thể cung cấp mảnh ghép còn thiếu khi cố gắng xây dựng các cuộc tấn công phức tạp, có mức độ nghiêm trọng cao.  

Thỉnh thoảng, thông tin nhạy cảm có thể bị rò rỉ một cách bất cẩn cho người dùng khi họ chỉ đơn giản là duyệt web một cách bình thường. Tuy nhiên, phổ biến hơn, kẻ tấn công cần phải lấy được thông tin bằng cách tương tác với trang web theo những cách bất ngờ hoặc độc hại. Sau đó, chúng sẽ nghiên cứu kỹ lưỡng phản hồi của trang web để cố gắng xác định các hành vi đáng chú ý.  

## Ví dụ về việc tiết lộ thông tin  
Dưới đây là một số ví dụ cơ bản về việc tiết lộ thông tin:

* Tiết lộ tên các thư mục ẩn, cấu trúc và nội dung của chúng thông qua danh sách tệp hoặc thư mục `robots.txt`.
* Cung cấp quyền truy cập vào các tệp mã nguồn thông qua các bản sao lưu tạm thời.
* Nêu rõ tên bảng hoặc cột trong thông báo lỗi.
* Tiết lộ thông tin nhạy cảm một cách không cần thiết, chẳng hạn như chi tiết thẻ tín dụng.
* Mã hóa cứng các khóa API, địa chỉ IP, thông tin đăng nhập cơ sở dữ liệu, v.v. trong mã nguồn.
* Gợi ý về sự tồn tại hoặc thiếu vắng các tài nguyên, tên người dùng, v.v. thông qua những khác biệt nhỏ trong hành vi của ứng dụng.  

# Các lỗ hổng tiết lộ thông tin phát sinh như thế nào?  
Các lỗ hổng tiết lộ thông tin có thể phát sinh theo vô số cách khác nhau, nhưng nhìn chung có thể được phân loại như sau:  
* Không loại bỏ nội dung nội bộ khỏi nội dung công khai 
* Cấu hình không an toàn của trang web và các công nghệ liên quan. Ví dụ, việc không vô hiệu hóa các tính năng gỡ lỗi và chẩn đoán đôi khi có thể cung cấp cho kẻ tấn công những công cụ hữu ích giúp chúng thu thập thông tin nhạy cảm. Cấu hình mặc định cũng có thể khiến các trang web dễ bị tổn thương, chẳng hạn như hiển thị các thông báo lỗi quá dài dòng.  
* Lỗi thiết kế và hoạt động của ứng dụng. Ví dụ, nếu một trang web trả về các phản hồi khác nhau khi xảy ra các trạng thái lỗi khác nhau, điều này cũng có thể cho phép kẻ tấn công thu thập dữ liệu nhạy cảm , chẳng hạn như thông tin đăng nhập hợp lệ của người dùng.  

# Các lỗ hổng bảo mật thông tin gây ra những ảnh hưởng như thế nào?  
Các lỗ hổng tiết lộ thông tin có thể gây ra cả tác động trực tiếp và gián tiếp tùy thuộc vào mục đích của trang web và do đó, loại thông tin mà kẻ tấn công có thể thu được. Trong một số trường hợp, chỉ riêng hành động tiết lộ thông tin nhạy cảm cũng có thể gây ra hậu quả nghiêm trọng cho các bên bị ảnh hưởng. Ví dụ, việc một cửa hàng trực tuyến làm rò rỉ thông tin thẻ tín dụng của khách hàng có thể dẫn đến những hậu quả nghiêm trọng.

Mặt khác, việc rò rỉ thông tin kỹ thuật, chẳng hạn như cấu trúc thư mục hoặc các framework của bên thứ ba đang được sử dụng, có thể không gây ra tác động trực tiếp đáng kể nào. Tuy nhiên, nếu rơi vào tay kẻ xấu, đây có thể là thông tin then chốt cần thiết để tạo ra vô số các lỗ hổng bảo mật khác. Mức độ nghiêm trọng trong trường hợp này phụ thuộc vào những gì kẻ tấn công có thể làm với thông tin đó.  

## Làm thế nào để đánh giá mức độ nghiêm trọng của các lỗ hổng tiết lộ thông tin?  
Mặc dù hậu quả cuối cùng có thể rất nghiêm trọng, nhưng chỉ trong những trường hợp cụ thể, việc tiết lộ thông tin mới trở thành vấn đề nghiêm trọng. Trong quá trình thử nghiệm, việc tiết lộ thông tin kỹ thuật nói riêng thường chỉ được quan tâm nếu bạn có thể chứng minh được kẻ tấn công có thể làm điều gì đó có hại với thông tin đó.

Ví dụ, việc biết một trang web đang sử dụng một phiên bản framework cụ thể sẽ không có nhiều ích lợi nếu phiên bản đó đã được vá lỗi hoàn toàn. Tuy nhiên, thông tin này trở nên quan trọng khi trang web đang sử dụng một phiên bản cũ chứa lỗ hổng bảo mật đã biết. Trong trường hợp này, việc thực hiện một cuộc tấn công tàn phá có thể đơn giản như việc áp dụng một mã khai thác đã được công khai.

Điều quan trọng là phải sử dụng lý trí và sự tỉnh táo khi phát hiện thông tin nhạy cảm bị rò rỉ. Rất có thể những chi tiết kỹ thuật nhỏ có thể bị phát hiện bằng nhiều cách khác nhau trên nhiều trang web mà bạn kiểm tra. Do đó, trọng tâm chính của bạn nên là tác động và khả năng bị khai thác của thông tin bị rò rỉ, chứ không chỉ là sự hiện diện của việc tiết lộ thông tin như một vấn đề riêng lẻ. Ngoại lệ rõ ràng là khi thông tin bị rò rỉ quá nhạy cảm đến mức cần được chú ý riêng.  

# Cách phòng ngừa các lỗ hổng tiết lộ thông tin  
Việc ngăn chặn hoàn toàn việc rò rỉ thông tin là rất khó khăn do có vô số cách thức xảy ra. Tuy nhiên, có một số biện pháp thực hành tốt nhất nói chung mà bạn có thể tuân theo để giảm thiểu rủi ro các loại lỗ hổng này xâm nhập vào trang web của mình.

* Hãy đảm bảo rằng tất cả những người tham gia sản xuất trang web đều hiểu rõ thông tin nào được coi là nhạy cảm. Đôi khi, những thông tin tưởng chừng vô hại lại có thể hữu ích hơn nhiều đối với kẻ tấn công so với những gì mọi người nhận ra. Việc nhấn mạnh những mối nguy hiểm này có thể giúp đảm bảo rằng thông tin nhạy cảm được xử lý an toàn hơn nói chung trong tổ chức của bạn.
* Kiểm tra mã nguồn để phát hiện khả năng tiết lộ thông tin như một phần của quy trình đảm bảo chất lượng hoặc xây dựng sản phẩm. Việc tự động hóa một số tác vụ liên quan, chẳng hạn như loại bỏ các bình luận của nhà phát triển, tương đối dễ dàng.
* Hãy sử dụng các thông báo lỗi chung chung nhất có thể. Đừng cung cấp cho kẻ tấn công những manh mối không cần thiết về hành vi của ứng dụng.
* Hãy kiểm tra kỹ xem tất cả các tính năng gỡ lỗi hoặc chẩn đoán đã bị vô hiệu hóa trong môi trường sản xuất hay chưa.
* Hãy đảm bảo bạn hiểu rõ các thiết lập cấu hình và những vấn đề bảo mật của bất kỳ công nghệ bên thứ ba nào mà bạn triển khai. Hãy dành thời gian tìm hiểu và vô hiệu hóa bất kỳ tính năng và cài đặt nào mà bạn thực sự không cần.

