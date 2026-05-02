# Cách kiểm tra các lỗ hổng tiết lộ thông tin  
Nhìn chung, điều quan trọng là không nên có "tầm nhìn hạn hẹp" trong quá trình kiểm thử. Nói cách khác, bạn nên tránh tập trung quá mức vào một lỗ hổng cụ thể. Dữ liệu nhạy cảm có thể bị rò rỉ ở nhiều nơi khác nhau, vì vậy điều quan trọng là không bỏ sót bất kỳ thông tin nào có thể hữu ích sau này. Bạn thường sẽ tìm thấy dữ liệu nhạy cảm trong khi kiểm thử một thứ khác. Một kỹ năng quan trọng là khả năng nhận biết thông tin thú vị bất cứ khi nào và ở bất cứ đâu bạn bắt gặp nó.

Dưới đây là một số ví dụ về các kỹ thuật và công cụ cấp cao mà bạn có thể sử dụng để giúp xác định các lỗ hổng tiết lộ thông tin trong quá trình thử nghiệm.  

## Fuzzing
Nếu bạn xác định được các tham số thú vị, bạn có thể thử gửi các kiểu dữ liệu không mong đợi và các chuỗi lỗi được tạo riêng để xem hiệu quả của chúng. Hãy chú ý kỹ; mặc dù đôi khi phản hồi tiết lộ rõ ​​ràng thông tin thú vị, chúng cũng có thể gợi ý về hành vi của ứng dụng một cách tinh tế hơn. Ví dụ, đó có thể là sự khác biệt nhỏ về thời gian xử lý yêu cầu. Ngay cả khi nội dung của thông báo lỗi không tiết lộ bất cứ điều gì, đôi khi việc gặp phải trường hợp lỗi này thay vì trường hợp lỗi khác cũng là thông tin hữu ích.

Bạn có thể tự động hóa phần lớn quy trình này bằng các công cụ như Burp Intruder. Điều này mang lại một số lợi ích. Quan trọng nhất, bạn có thể:

* Thêm vị trí tải trọng vào các tham số và sử dụng danh sách từ có sẵn của các chuỗi kiểm thử để kiểm tra một lượng lớn các đầu vào khác nhau một cách nhanh chóng.
* Dễ dàng xác định sự khác biệt trong phản hồi bằng cách so sánh mã trạng thái HTTP, thời gian phản hồi, độ dài, v.v.
* Sử dụng các quy tắc khớp của grep để nhanh chóng xác định sự xuất hiện của các từ khóa, chẳng hạn như error, invalid, SELECT, SQL, v.v.
* Áp dụng các quy tắc trích xuất grep để trích xuất và so sánh nội dung của các mục quan trọng trong phản hồi.  

## Sử dụng Burp Scanner  
Người dùng Burp Suite Professional được hưởng lợi từ Burp Scanner. Công cụ này cung cấp tính năng quét trực tiếp để kiểm tra các mục trong khi bạn duyệt web, hoặc bạn có thể lên lịch quét tự động để thu thập thông tin và kiểm tra trang web mục tiêu thay mặt bạn. Cả hai phương pháp đều sẽ tự động gắn cờ nhiều lỗ hổng tiết lộ thông tin cho bạn. Ví dụ, Burp Scanner sẽ cảnh báo bạn nếu tìm thấy thông tin nhạy cảm như khóa riêng tư, địa chỉ email và số thẻ tín dụng trong phản hồi. Nó cũng sẽ xác định bất kỳ tệp sao lưu, danh sách thư mục, v.v.  

## Sử dụng các công cụ tương tác của Burp  
Burp cung cấp một số công cụ tương tác mà bạn có thể sử dụng để dễ dàng tìm thấy thông tin thú vị trên trang web mục tiêu. Bạn có thể truy cập các công cụ tương tác từ menu ngữ cảnh - chỉ cần nhấp chuột phải vào bất kỳ thông báo HTTP nào, mục Burp Proxy hoặc mục nào trong sơ đồ trang web và chọn "Engagement tools".

Các công cụ sau đây đặc biệt hữu ích trong bối cảnh này.  

### Search
Bạn có thể sử dụng công cụ này để tìm kiếm bất kỳ biểu thức nào trong mục đã chọn. Bạn có thể tinh chỉnh kết quả bằng nhiều tùy chọn tìm kiếm nâng cao, chẳng hạn như tìm kiếm biểu thức chính quy hoặc tìm kiếm phủ định. Điều này rất hữu ích để nhanh chóng tìm thấy sự xuất hiện (hoặc vắng mặt) của các từ khóa cụ thể mà bạn quan tâm.  

### Find comments  
Bạn có thể sử dụng công cụ này để nhanh chóng trích xuất bất kỳ nhận xét nào của nhà phát triển được tìm thấy trong mục đã chọn. Nó cũng cung cấp các tab để truy cập ngay lập tức vào chu kỳ yêu cầu/phản hồi HTTP mà trong đó mỗi nhận xét được tìm thấy.

### Discover content  
Bạn có thể sử dụng công cụ này để xác định nội dung và chức năng bổ sung không được liên kết từ nội dung hiển thị trên trang web. Điều này có thể hữu ích để tìm các thư mục và tệp bổ sung mà không nhất thiết phải tự động xuất hiện trong sơ đồ trang web.  

## Phản hồi mang tính thông tin về kỹ thuật  
Đôi khi, các thông báo lỗi chi tiết có thể tiết lộ những thông tin thú vị trong quá trình kiểm thử thông thường của bạn. Tuy nhiên, bằng cách nghiên cứu cách các thông báo lỗi thay đổi tùy thuộc vào dữ liệu đầu vào, bạn có thể tiến thêm một bước nữa. Trong một số trường hợp, bạn có thể thao túng trang web để trích xuất dữ liệu tùy ý thông qua thông báo lỗi.

Có rất nhiều phương pháp để thực hiện điều này tùy thuộc vào tình huống cụ thể mà bạn gặp phải. Một ví dụ phổ biến là khiến logic ứng dụng cố gắng thực hiện một hành động không hợp lệ trên một mục dữ liệu cụ thể. Ví dụ, việc gửi một giá trị tham số không hợp lệ có thể dẫn đến một dấu vết ngăn xếp hoặc phản hồi gỡ lỗi chứa các chi tiết thú vị. Đôi khi bạn có thể khiến các thông báo lỗi tiết lộ giá trị của dữ liệu mong muốn trong phản hồi.

# Các nguồn thông tin phổ biến được tiết lộ  
Việc tiết lộ thông tin có thể xảy ra trong nhiều bối cảnh khác nhau trên một trang web. Sau đây là một số ví dụ phổ biến về những nơi bạn có thể kiểm tra xem thông tin nhạy cảm có bị lộ hay không.  

## Các tập tin dành cho trình thu thập dữ liệu web  
Nhiều trang web cung cấp các tập tin tại `/robots.txt` và `/sitemap.xml` để giúp trình thu thập thông tin điều hướng trang web của họ. Trong số những thứ khác, các tập tin này thường liệt kê các thư mục cụ thể mà trình thu thập thông tin nên bỏ qua, ví dụ, vì chúng có thể chứa thông tin nhạy cảm.

Vì các tệp này thường không được liên kết từ bên trong trang web, chúng có thể không xuất hiện ngay lập tức trong sơ đồ trang web của Burp. Tuy nhiên, bạn nên thử điều hướng đến đó `/robots.txt` hoặc `/sitemap.xml` tìm kiếm thủ công để xem có tìm thấy bất kỳ thông tin hữu ích nào không.  

## Danh sách thư mục  
Máy chủ web có thể được cấu hình để tự động liệt kê nội dung của các thư mục không có trang chỉ mục. Điều này có thể hỗ trợ kẻ tấn công bằng cách cho phép chúng nhanh chóng xác định các tài nguyên tại một đường dẫn nhất định, và tiến hành phân tích và tấn công trực tiếp các tài nguyên đó. Đặc biệt, nó làm tăng nguy cơ lộ các tệp nhạy cảm trong thư mục mà người dùng không được phép truy cập, chẳng hạn như các tệp tạm thời và các bản ghi lỗi hệ thống.

Bản thân các danh sách thư mục không nhất thiết là một lỗ hổng bảo mật. Tuy nhiên, nếu trang web cũng không thực hiện kiểm soát truy cập đúng cách, thì việc rò rỉ sự tồn tại và vị trí của các tài nguyên nhạy cảm theo cách này rõ ràng là một vấn đề.  

## Bình luận của nhà phát triển  
Trong quá trình phát triển, đôi khi các chú thích HTML nội tuyến được thêm vào mã đánh dấu. Thông thường, các chú thích này sẽ bị loại bỏ trước khi các thay đổi được triển khai lên môi trường sản xuất. Tuy nhiên, đôi khi các chú thích có thể bị quên, bỏ sót hoặc thậm chí được giữ lại một cách cố ý vì người tạo ra chúng không hoàn toàn nhận thức được các vấn đề bảo mật. Mặc dù các chú thích này không hiển thị trên trang được kết xuất, nhưng chúng có thể dễ dàng được truy cập bằng Burp hoặc thậm chí là các công cụ dành cho nhà phát triển được tích hợp sẵn của trình duyệt.

Đôi khi, những bình luận này chứa thông tin hữu ích cho kẻ tấn công. Ví dụ, chúng có thể gợi ý về sự tồn tại của các thư mục ẩn hoặc cung cấp manh mối về logic ứng dụng.  

## Thông báo lỗi  
Một trong những nguyên nhân phổ biến nhất gây ra rò rỉ thông tin là các thông báo lỗi quá dài dòng. Theo nguyên tắc chung, bạn nên chú ý kỹ đến tất cả các thông báo lỗi gặp phải trong quá trình kiểm toán.

Nội dung của các thông báo lỗi có thể tiết lộ thông tin về loại dữ liệu hoặc kiểu dữ liệu đầu vào được mong đợi từ một tham số nhất định. Điều này có thể giúp bạn thu hẹp phạm vi tấn công bằng cách xác định các tham số có thể bị khai thác. Thậm chí, nó có thể giúp bạn tránh lãng phí thời gian cố gắng chèn các payload mà đơn giản là không hoạt động.

Các thông báo lỗi chi tiết cũng có thể cung cấp thông tin về các công nghệ khác nhau mà trang web đang sử dụng. Ví dụ, chúng có thể nêu rõ tên công cụ tạo mẫu, loại cơ sở dữ liệu hoặc máy chủ mà trang web đang sử dụng, cùng với số phiên bản của nó. Thông tin này rất hữu ích vì bạn có thể dễ dàng tìm kiếm bất kỳ lỗ hổng bảo mật nào đã được ghi nhận cho phiên bản này. Tương tự, bạn có thể kiểm tra xem có bất kỳ lỗi cấu hình phổ biến hoặc cài đặt mặc định nguy hiểm nào mà bạn có thể khai thác hay không. Một số lỗi này có thể được nêu bật trong tài liệu chính thức.

Bạn cũng có thể phát hiện ra rằng trang web đang sử dụng một loại khung phần mềm mã nguồn mở nào đó. Trong trường hợp này, bạn có thể nghiên cứu mã nguồn được công khai, đây là một nguồn tài nguyên vô giá để xây dựng các công cụ khai thác của riêng mình.

Sự khác biệt giữa các thông báo lỗi cũng có thể tiết lộ các hành vi khác nhau của ứng dụng đang diễn ra ngầm. Quan sát sự khác biệt trong các thông báo lỗi là một khía cạnh quan trọng của nhiều kỹ thuật, chẳng hạn như tấn công SQL injection, liệt kê tên người dùng, ...vv  

#### Thực hành: Tiết lộ thông tin trong thông báo lỗi
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Information_disclosure/Solution/lab1.py)  

## Gỡ lỗi dữ liệu  
Để phục vụ mục đích gỡ lỗi, nhiều trang web tạo ra các thông báo lỗi và nhật ký tùy chỉnh chứa lượng lớn thông tin về hoạt động của ứng dụng. Mặc dù thông tin này hữu ích trong quá trình phát triển, nhưng nó cũng cực kỳ có lợi cho kẻ tấn công nếu bị rò rỉ trong môi trường sản xuất.

Các thông báo gỡ lỗi đôi khi có thể chứa thông tin quan trọng để phát triển một cuộc tấn công, bao gồm:

Các giá trị cho các biến phiên quan trọng có thể được thao tác thông qua đầu vào của người dùng.
Tên máy chủ và thông tin đăng nhập cho các thành phần phụ trợ
Tên tệp và thư mục trên máy chủ
Các khóa được sử dụng để mã hóa dữ liệu được truyền qua máy khách.
Thông tin gỡ lỗi đôi khi được ghi vào một tệp riêng biệt. Nếu kẻ tấn công có thể truy cập vào tệp này, nó có thể là tài liệu tham khảo hữu ích để hiểu trạng thái hoạt động của ứng dụng. Nó cũng có thể cung cấp một số manh mối về cách chúng có thể cung cấp dữ liệu đầu vào được tạo ra để thao túng trạng thái ứng dụng và kiểm soát thông tin nhận được.  

#### Thực hành: Công bố thông tin trên trang gỡ lỗi  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Information_disclosure/Solution/lab2.py)  

## Trang tài khoản người dùng  
Về bản chất, trang hồ sơ hoặc trang tài khoản người dùng thường chứa thông tin nhạy cảm, chẳng hạn như địa chỉ email, số điện thoại, khóa API, v.v. Vì người dùng thường chỉ có quyền truy cập vào trang tài khoản của riêng họ, nên điều này tự nó không phải là một lỗ hổng bảo mật. Tuy nhiên, một số trang web chứa các lỗi logic có khả năng cho phép kẻ tấn công lợi dụng các trang này để xem dữ liệu của người dùng khác.

Ví dụ, hãy xem xét một trang web xác định trang tài khoản của người dùng nào sẽ được tải dựa trên một `user` tham số.

GET /user/personal-info?user=carlos`
Hầu hết các trang web sẽ thực hiện các biện pháp để ngăn chặn kẻ tấn công chỉ cần thay đổi tham số này để truy cập vào trang tài khoản của người dùng bất kỳ. Tuy nhiên, đôi khi logic để tải các mục dữ liệu riêng lẻ không được mạnh mẽ cho lắm.

Kẻ tấn công có thể không tải được toàn bộ trang tài khoản của người dùng khác, nhưng logic để lấy và hiển thị địa chỉ email đã đăng ký của người dùng, chẳng hạn, có thể không kiểm tra xem tham `user` số có khớp với người dùng hiện đang đăng nhập hay không. Trong trường hợp này, chỉ cần thay đổi tham `user` số là kẻ tấn công có thể hiển thị địa chỉ email của bất kỳ người dùng nào trên trang tài khoản của chính họ.

Chúng ta sẽ xem xét chi tiết hơn về các loại lỗ hổng này khi đề cập đến các lỗ hổng kiểm soát truy cập và IDOR.  

## Việc tiết lộ mã nguồn thông qua các tập tin sao lưu.  
Việc có được quyền truy cập mã nguồn giúp kẻ tấn công dễ dàng hiểu được hành vi của ứng dụng và xây dựng các cuộc tấn công có mức độ nghiêm trọng cao. Dữ liệu nhạy cảm đôi khi thậm chí còn được mã hóa cứng trong mã nguồn. Ví dụ điển hình bao gồm khóa API và thông tin đăng nhập để truy cập các thành phần phụ trợ.

Nếu bạn có thể xác định được một công nghệ mã nguồn mở cụ thể đang được sử dụng, điều này sẽ giúp bạn dễ dàng truy cập vào một lượng mã nguồn hạn chế.

Thỉnh thoảng, thậm chí có thể khiến trang web tự lộ mã nguồn của nó. Khi lập sơ đồ một trang web, bạn có thể thấy một số tệp mã nguồn được tham chiếu rõ ràng. Tuy nhiên, việc yêu cầu chúng thường không tiết lộ được chính mã nguồn đó. Khi máy chủ xử lý các tệp có phần mở rộng cụ thể, chẳng hạn như `.php`, nó thường sẽ thực thi mã, thay vì chỉ gửi nó cho máy khách dưới dạng văn bản. Tuy nhiên, trong một số trường hợp, bạn có thể đánh lừa trang web để nó trả về nội dung của tệp. Ví dụ, các trình soạn thảo văn bản thường tạo các tệp sao lưu tạm thời trong khi tệp gốc đang được chỉnh sửa. Các tệp tạm thời này thường được chỉ định bằng một số cách, chẳng hạn như bằng cách thêm dấu ngã (`~`) vào tên tệp hoặc thêm phần mở rộng tệp khác. Yêu cầu một tệp mã bằng cách sử dụng phần mở rộng tệp sao lưu đôi khi có thể cho phép bạn đọc nội dung của tệp trong phản hồi.  

Một khi kẻ tấn công có quyền truy cập vào mã nguồn, đây có thể là một bước tiến lớn giúp chúng xác định và khai thác thêm các lỗ hổng mà nếu không thì gần như không thể thực hiện được. Một ví dụ điển hình là lỗi giải mã dữ liệu không an toàn. Chúng ta sẽ xem xét lỗ hổng này trong một chủ đề riêng biệt sau.  

#### Thực hành: Lộ mã nguồn thông qua các tập tin sao lưu.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Information_disclosure/Solution/lab3.py)   

