# Cross-site scripting(XSS) là gì
Tấn công kịch bản chéo trang (còn gọi là XSS) là một lỗ hổng bảo mật web cho phép kẻ tấn công xâm phạm các tương tác của người dùng với ứng dụng dễ bị tổn thương. Nó cho phép kẻ tấn công vượt qua chính sách cùng nguồn gốc, được thiết kế để phân tách các trang web khác nhau. Lỗ hổng kịch bản chéo trang thường cho phép kẻ tấn công giả mạo người dùng nạn nhân, thực hiện bất kỳ hành động nào mà người dùng có thể thực hiện và truy cập bất kỳ dữ liệu nào của người dùng. Nếu người dùng nạn nhân có quyền truy cập đặc quyền trong ứng dụng, thì kẻ tấn công có thể giành được quyền kiểm soát hoàn toàn tất cả chức năng và dữ liệu của ứng dụng.  

# XSS hoạt động như thế nào?  
Tấn công kịch bản chéo trang hoạt động bằng cách thao túng một trang web dễ bị tổn thương để nó trả về mã JavaScript độc hại cho người dùng. Khi mã độc hại được thực thi bên trong trình duyệt của nạn nhân, kẻ tấn công có thể hoàn toàn xâm phạm trải nghiệm tương tác của họ với ứng dụng.

# Bằng chứng về khả năng tấn công XSS  
Bạn có thể xác nhận hầu hết các loại lỗ hổng XSS bằng cách chèn một đoạn mã độc khiến trình duyệt của bạn thực thi một đoạn mã JavaScript tùy ý. Từ lâu, việc sử dụng hàm `alert()` này đã trở nên phổ biến vì nó ngắn gọn, vô hại và khá khó để bỏ sót khi được gọi thành công. Trên thực tế, bạn giải quyết phần lớn các bài thực hành XSS của chúng tôi bằng cách gọi hàm `alert()` này trong trình duyệt của nạn nhân giả lập.

Thật không may, sẽ có một chút trục trặc nếu bạn sử dụng Chrome. Từ phiên bản 92 trở đi (ngày 20 tháng 7 năm 2021), iframe đa nguồn gốc sẽ bị chặn gọi hàm ` alert().`. Vì chúng được sử dụng để xây dựng một số cuộc tấn công XSS nâng cao hơn, đôi khi bạn sẽ cần sử dụng một payload PoC thay thế. Trong trường hợp này, chúng tôi khuyên bạn nên sử dụng hàm ` print().`. Nếu bạn muốn tìm hiểu thêm về thay đổi này và lý do tại sao chúng tôi thích ` print().`, hãy xem bài đăng trên blog của chúng tôi về chủ đề này.

Vì nạn nhân giả lập trong phòng thí nghiệm của chúng tôi sử dụng Chrome, chúng tôi đã sửa đổi các bài tập trong phòng thí nghiệm bị ảnh hưởng để chúng cũng có thể được giải quyết bằng print()trình duyệt này. Chúng tôi đã chỉ rõ điều này trong hướng dẫn ở những chỗ cần thiết.

# Các loại tấn công XSS là gì?  
Có ba loại tấn công XSS chính. Đó là:

* [Lỗ hổng XSS reflected](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Reflected_XSS.md), trong đó mã độc được chèn thông qua yêu cầu HTTP hiện tại (ví dụ: URL, tham số tìm kiếm, v.v.).
* [Lỗ hổng XSS Stored](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Stored_XSS.md), trong đó mã độc được lưu trữ trên máy chủ (ví dụ: bình luận, bài đăng, v.v.).
* [Lỗ hổng XSS DOM](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/DOM-based_XSS.md), trong đó điểm yếu nằm ở mã phía máy khách.

# Tấn công XSS Reflected
Tấn công XSS reflected là dạng đơn giản nhất của tấn công kịch bản chéo trang. Nó xảy ra khi một ứng dụng nhận dữ liệu trong một yêu cầu HTTP và đưa dữ liệu đó vào phản hồi ngay lập tức theo cách không an toàn.

Dưới đây là một ví dụ đơn giản về lỗ hổng XSS reflected:  

```
https://insecure-website.com/status?message=All+is+well.
<p>Status: All is well.</p>
```

Ứng dụng không thực hiện bất kỳ quá trình xử lý dữ liệu nào khác, vì vậy kẻ tấn công có thể dễ dàng tạo ra một cuộc tấn công như sau:  

```
https://insecure-website.com/status?message=<script>/*+Bad+stuff+here...+*/</script>
<p>Status: <script>/* Bad stuff here... */</script></p>
```

Nếu người dùng truy cập vào URL do kẻ tấn công tạo ra, thì kịch bản của kẻ tấn công sẽ được thực thi trong trình duyệt của người dùng, trong ngữ cảnh phiên làm việc của người dùng với ứng dụng. Tại thời điểm đó, kịch bản có thể thực hiện bất kỳ hành động nào và truy xuất bất kỳ dữ liệu nào mà người dùng có quyền truy cập.  

# Tấn công XSS Stored
Lỗ hổng XSS lưu trữ (còn được gọi là XSS dai dẳng hoặc XSS bậc hai) phát sinh khi một ứng dụng nhận dữ liệu từ một nguồn không đáng tin cậy và đưa dữ liệu đó vào các phản hồi HTTP sau đó một cách không an toàn.

Dữ liệu được đề cập có thể được gửi đến ứng dụng thông qua các yêu cầu HTTP; ví dụ: bình luận trên bài đăng blog, biệt danh người dùng trong phòng trò chuyện hoặc thông tin liên hệ trên đơn đặt hàng của khách hàng. Trong các trường hợp khác, dữ liệu có thể đến từ các nguồn không đáng tin cậy khác; ví dụ: ứng dụng webmail hiển thị tin nhắn nhận được qua SMTP, ứng dụng tiếp thị hiển thị bài đăng trên mạng xã hội hoặc ứng dụng giám sát mạng hiển thị dữ liệu gói từ lưu lượng mạng.

Dưới đây là một ví dụ đơn giản về lỗ hổng XSS lưu trữ. Một ứng dụng diễn đàn cho phép người dùng gửi tin nhắn, và những tin nhắn này sẽ được hiển thị cho những người dùng khác:  

`<p>Hello, this is my message!</p>`  

Ứng dụng không thực hiện bất kỳ quá trình xử lý dữ liệu nào khác, vì vậy kẻ tấn công có thể dễ dàng gửi tin nhắn tấn công người dùng khác:  

`<p><script>/* Bad stuff here... */</script></p>`  

# Tấn công XSS DOM
Lỗ hổng XSS dựa trên DOM (còn được gọi là DOM XSS) phát sinh khi một ứng dụng chứa một số mã JavaScript phía máy khách xử lý dữ liệu từ một nguồn không đáng tin cậy theo cách không an toàn, thường là bằng cách ghi dữ liệu trở lại DOM.

Trong ví dụ sau, một ứng dụng sử dụng JavaScript để đọc giá trị từ một trường nhập liệu và ghi giá trị đó vào một phần tử trong HTML:  

```javascript
var search = document.getElementById('search').value;
var results = document.getElementById('results');
results.innerHTML = 'You searched for: ' + search;
```

Nếu kẻ tấn công có thể kiểm soát giá trị của trường nhập liệu, chúng có thể dễ dàng tạo ra một giá trị độc hại khiến kịch bản của chúng được thực thi:  

`You searched for: <img src=1 onerror='/* Bad stuff here... */'>`  

Trong trường hợp điển hình, trường nhập liệu sẽ được điền thông tin từ một phần của yêu cầu HTTP, chẳng hạn như tham số chuỗi truy vấn URL, cho phép kẻ tấn công thực hiện cuộc tấn công bằng cách sử dụng URL độc hại, theo cùng một cách như tấn công XSS reflected.  

# XSS có thể được sử dụng cho mục đích gì?  
Kẻ tấn công khai thác lỗ hổng kịch bản chéo trang (cross-site scripting) thường có thể:

* Giả mạo hoặc mạo danh người dùng là nạn nhân.
* Thực hiện bất kỳ hành động nào mà người dùng có khả năng thực hiện.
* Đọc bất kỳ dữ liệu nào mà người dùng có thể truy cập.
* Thu thập thông tin đăng nhập của người dùng.
* Thực hiện tấn công làm biến dạng trang web ảo.
* Chèn mã độc Trojan vào trang web.  

# Tác động của các lỗ hổng XSS  
Tác động thực tế của một cuộc tấn công XSS thường phụ thuộc vào bản chất của ứng dụng, chức năng và dữ liệu của nó, cũng như trạng thái của người dùng bị xâm phạm. Ví dụ:

* Trong một ứng dụng dạng brochure, nơi tất cả người dùng đều ẩn danh và tất cả thông tin đều công khai, tác động thường sẽ ở mức tối thiểu.
* Trong một ứng dụng lưu trữ dữ liệu nhạy cảm, chẳng hạn như giao dịch ngân hàng, email hoặc hồ sơ y tế, tác động thường sẽ rất nghiêm trọng.
* Nếu người dùng bị xâm phạm có quyền quản trị cao trong ứng dụng, thì hậu quả thường sẽ rất nghiêm trọng, cho phép kẻ tấn công giành quyền kiểm soát hoàn toàn ứng dụng dễ bị tổn thương và xâm phạm tất cả người dùng cũng như dữ liệu của họ.  

# Cách tìm và kiểm tra lỗ hổng XSS  
Đa số các lỗ hổng XSS có thể được phát hiện nhanh chóng và đáng tin cậy bằng cách sử dụng công cụ quét lỗ hổng web của Burp Suite.

Việc kiểm tra thủ công lỗ hổng XSS reflected và stored thường bao gồm việc gửi một chuỗi ký tự đơn giản, duy nhất (chẳng hạn như một chuỗi ký tự chữ và số ngắn) vào mọi điểm truy cập trong ứng dụng, xác định mọi vị trí mà dữ liệu đầu vào được trả về trong phản hồi HTTP, và kiểm tra từng vị trí riêng lẻ để xác định xem dữ liệu đầu vào được tạo ra phù hợp có thể được sử dụng để thực thi mã JavaScript tùy ý hay không. Bằng cách này, bạn có thể xác định ngữ cảnh xảy ra lỗ hổng XSS và chọn một payload phù hợp để khai thác nó.

Việc kiểm tra thủ công các lỗ hổng XSS dựa trên DOM phát sinh từ các tham số URL bao gồm một quy trình tương tự: đặt một đoạn mã đầu vào duy nhất đơn giản vào tham số, sử dụng công cụ dành cho nhà phát triển của trình duyệt để tìm kiếm đoạn mã đầu vào này trong DOM và kiểm tra từng vị trí để xác định xem nó có thể bị khai thác hay không. Tuy nhiên, các loại lỗ hổng XSS dựa trên DOM khác khó phát hiện hơn. Để tìm các lỗ hổng dựa trên DOM trong các đầu vào không dựa trên URL (chẳng hạn như `document.cookie`) hoặc các đích đến không dựa trên HTML (như `setTimeout`), không có gì thay thế được việc xem xét mã JavaScript, điều này có thể cực kỳ tốn thời gian. Trình quét lỗ hổng web của Burp Suite kết hợp phân tích tĩnh và động của JavaScript để tự động phát hiện các lỗ hổng dựa trên DOM một cách đáng tin cậy.  

# Chính sách bảo mật nội dung  
Chính sách bảo mật nội dung (CSP) là một cơ chế của trình duyệt nhằm giảm thiểu tác động của tấn công kịch bản chéo trang (XSS) và một số lỗ hổng khác. Nếu một ứng dụng sử dụng CSP chứa hành vi tương tự XSS, thì CSP có thể cản trở hoặc ngăn chặn việc khai thác lỗ hổng. Tuy nhiên, CSP thường có thể bị vượt qua để khai thác lỗ hổng tiềm ẩn.  

# Dangling markup injection  
Dangling markup injection là một dạng lỗ hổng XSS nơi dữ liệu độc hại được chèn vào một thẻ chưa đóng (dangling tag), làm thay đổi cách trình duyệt phân tích cú pháp HTML, dẫn đến việc thực thi mã độc. Kỹ thuật này thường có thể bị khai thác để thu thập thông tin nhạy cảm mà người dùng khác có thể nhìn thấy, bao gồm cả mã thông báo CSRF có thể được sử dụng để thực hiện các hành động trái phép thay mặt người dùng.  

# Cách phòng chống tấn công XSS  
Ngăn chặn tấn công kịch bản chéo trang (cross-site scripting) có thể khá đơn giản trong một số trường hợp, nhưng lại khó khăn hơn nhiều tùy thuộc vào độ phức tạp của ứng dụng và cách thức xử lý dữ liệu do người dùng kiểm soát.

Nhìn chung, việc ngăn chặn hiệu quả các lỗ hổng XSS thường bao gồm sự kết hợp của các biện pháp sau:

* **Lọc dữ liệu đầu vào ngay khi nhận được**. Tại thời điểm nhận được dữ liệu đầu vào từ người dùng, hãy lọc càng kỹ càng tốt dựa trên những gì được mong đợi hoặc là dữ liệu đầu vào hợp lệ.
* **Mã hóa dữ liệu khi xuất ra**. Tại thời điểm dữ liệu do người dùng kiểm soát được xuất ra trong phản hồi HTTP, hãy mã hóa dữ liệu đầu ra để ngăn nó bị hiểu nhầm là nội dung hoạt động. Tùy thuộc vào ngữ cảnh đầu ra, điều này có thể yêu cầu áp dụng kết hợp mã hóa HTML, URL, JavaScript và CSS.
* **Hãy sử dụng các tiêu đề phản hồi phù hợp**. Để ngăn chặn XSS trong các phản hồi HTTP không nhằm mục đích chứa bất kỳ HTML hoặc JavaScript nào, bạn có thể sử dụng các tiêu đề `Content-Type` và `X-Content-Type-Options` để đảm bảo rằng trình duyệt diễn giải các phản hồi theo cách bạn mong muốn.
* **Chính sách bảo mật nội dung**. Như một biện pháp phòng vệ cuối cùng, bạn có thể sử dụng Chính sách bảo mật nội dung (CSP) để giảm mức độ nghiêm trọng của bất kỳ lỗ hổng XSS nào vẫn còn xảy ra.  



