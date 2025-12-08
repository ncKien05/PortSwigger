# SQL Injection
Trong phần này, chúng tôi giải thích:  
* SQL injection (SQLi) là gì?  
* Cách tìm và khai thác các loại lỗ hổng SQLi khác nhau.  
* Làm thế nào để ngăn chặn SQLi.  
## SQL injection (SQLi) là gì?  
* SQL Injection (SQLi) là một lỗ hổng bảo mật web cho phép kẻ tấn công can thiệp vào các truy vấn mà ứng dụng thực hiện đối với cơ sở dữ liệu. Điều này có thể cho phép kẻ tấn công xem dữ liệu mà thông thường chúng không thể truy xuất. Dữ liệu này có thể bao gồm dữ liệu thuộc về người dùng khác hoặc bất kỳ dữ liệu nào khác mà ứng dụng có thể truy cập. Trong nhiều trường hợp, kẻ tấn công có thể sửa đổi hoặc xóa dữ liệu này, gây ra những thay đổi liên tục đối với nội dung hoặc hành vi của ứng dụng.  
  
* Trong một số trường hợp, kẻ tấn công có thể leo thang tấn công SQL injection để xâm nhập máy chủ hoặc cơ sở hạ tầng back-end khác. Điều này cũng có thể cho phép chúng thực hiện các cuộc tấn công từ chối dịch vụ.  
## Tác động của một cuộc tấn công SQL injection thành công là gì?  
Một cuộc tấn công tiêm SQL thành công có thể dẫn đến truy cập trái phép vào dữ liệu nhạy cảm, chẳng hạn như:  
  * Mật khẩu.  
  * Chi tiết thẻ tín dụng.  
  * Thông tin cá nhân của người dùng.  

Các cuộc tấn công tiêm nhiễm SQL đã được sử dụng trong nhiều vụ vi phạm dữ liệu nghiêm trọng trong nhiều năm qua. Chúng đã gây ra thiệt hại về uy tín và các khoản phạt theo quy định. Trong một số trường hợp, kẻ tấn công có thể xâm nhập vào hệ thống của tổ chức, dẫn đến một sự xâm phạm lâu dài mà không bị phát hiện trong một thời gian dài.  
## Cách phát hiện lỗ hổng SQL injection  
Bạn có thể phát hiện SQL Injection theo cách thủ công bằng cách sử dụng một bộ kiểm tra có hệ thống trên mọi điểm vào của ứng dụng. Để làm điều này, bạn thường sẽ gửi:
* Ký tự dấu nháy đơn `'` và tìm kiếm lỗi hoặc các bất thường khác.
* Một số cú pháp SQL cụ thể đánh giá theo giá trị cơ sở (gốc) của điểm vào và theo một giá trị khác, đồng thời tìm kiếm sự khác biệt có hệ thống trong phản hồi của ứng dụng.
* Các điều kiện Boolean như `OR 1=1` và `OR 1=2`  , và tìm kiếm sự khác biệt trong phản hồi của ứng dụng.
* Tải trọng được thiết kế để kích hoạt độ trễ thời gian khi thực hiện trong truy vấn SQL và tìm kiếm sự khác biệt về thời gian phản hồi.  
* Tải trọng OAST được thiết kế để kích hoạt tương tác mạng ngoài băng tần khi được thực hiện trong truy vấn SQL và giám sát mọi tương tác phát sinh.  

Ngoài ra, bạn có thể tìm thấy phần lớn các lỗ hổng SQL injection một cách nhanh chóng và đáng tin cậy bằng Burp Scanner.  

## Tiêm SQL vào các phần khác nhau của truy vấn  
Hầu hết các lỗ hổng SQL injection đều xảy ra trong WHEREmệnh đề của một SELECTtruy vấn. Hầu hết các kiểm thử viên giàu kinh nghiệm đều quen thuộc với loại SQL injection này.  
  
Tuy nhiên, lỗ hổng SQL injection có thể xảy ra ở bất kỳ vị trí nào trong truy vấn và trong nhiều loại truy vấn khác nhau. Một số vị trí phổ biến khác mà SQL injection phát sinh là:  
  
* Trong `UPDATE` các câu lệnh, trong các giá trị được cập nhật hoặc mệnh `WHERE` đề.
* Trong `INSERT` các câu lệnh, bên trong các giá trị được chèn vào.
* Trong `SELECT` các câu lệnh, bên trong tên bảng hoặc cột.
* Trong `SELECT` các câu lệnh, trong `ORDER BY` mệnh đề.
## Truy xuất dữ liệu ẩn  
Hãy tưởng tượng một ứng dụng mua sắm hiển thị sản phẩm theo nhiều danh mục khác nhau. Khi người dùng nhấp vào danh mục Quà tặng , trình duyệt của họ sẽ yêu cầu URL:  
`https://insecure-website.com/products?category=Gifts`  
Điều này khiến ứng dụng thực hiện truy vấn SQL để lấy thông tin chi tiết về các sản phẩm có liên quan từ cơ sở dữ liệu:  
`SELECT * FROM products WHERE category = 'Gifts' AND released = 1`  

Truy vấn SQL này yêu cầu cơ sở dữ liệu trả về:  
* tất cả các chi tiết ( *)
* từ bảng product
* nơi category = Gifts
* và released = 1.  
Hạn chế này `released = 1` được sử dụng để ẩn các sản phẩm chưa được phát hành. Chúng ta có thể giả định đối với các sản phẩm chưa được phát hành, `released = 0`

Ứng dụng không triển khai bất kỳ biện pháp phòng thủ nào chống lại các cuộc tấn công SQL injection. Điều này có nghĩa là kẻ tấn công có thể thực hiện các cuộc tấn công sau, ví dụ:  
`https://insecure-website.com/products?category=Gifts'--`  

Điều này dẫn đến truy vấn SQL:  
`SELECT * FROM products WHERE category = 'Gifts'--' AND released = 1`  

Quan trọng hơn, hãy lưu ý rằng đây `--` là một chỉ báo chú thích trong SQL. Điều này có nghĩa là phần còn lại của truy vấn được hiểu là một chú thích, về cơ bản là loại bỏ nó. Trong ví dụ này, điều này có nghĩa là truy vấn không còn chứa `AND released = 1`. Kết quả là, tất cả các sản phẩm đều được hiển thị, bao gồm cả những sản phẩm chưa được phát hành.  

Bạn có thể sử dụng một cuộc tấn công tương tự để khiến ứng dụng hiển thị tất cả các sản phẩm trong bất kỳ danh mục nào, bao gồm cả những danh mục mà ứng dụng không biết:  

`https://insecure-website.com/products?category=Gifts'+OR+1=1--`  

Điều này dẫn đến truy vấn SQL:

`SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1`  

* Cảnh báo:  
Hãy cẩn thận khi chèn điều kiện `OR 1=1` vào truy vấn SQL. Ngay cả khi điều kiện có vẻ vô hại trong ngữ cảnh bạn đang chèn, các ứng dụng thường sử dụng dữ liệu từ một yêu cầu duy nhất trong nhiều truy vấn khác nhau. Ví dụ: nếu điều kiện của bạn đạt đến câu lệnh `UPDATE` hoặc `DELETE`, điều đó có thể dẫn đến mất dữ liệu ngoài ý muốn.  
### Phòng thí nghiệm: Lỗ hổng SQL injection trong mệnh đề WHERE cho phép truy xuất dữ liệu ẩn
[Solution](./lab1.py)
## Lật đổ logic ứng dụng
Hãy tưởng tượng một ứng dụng cho phép người dùng đăng nhập bằng tên người dùng và mật khẩu. Nếu người dùng nhập tên người dùng `wiener` và mật khẩu `bluecheese` , ứng dụng sẽ kiểm tra thông tin đăng nhập bằng cách thực hiện truy vấn SQL sau:  

`SELECT * FROM users WHERE username = 'wiener' AND password = 'bluecheese'`
Nếu truy vấn trả về thông tin chi tiết của người dùng, thì đăng nhập thành công. Nếu không, đăng nhập sẽ bị từ chối.

Trong trường hợp này, kẻ tấn công có thể đăng nhập bằng bất kỳ người dùng nào mà không cần mật khẩu. Chúng có thể thực hiện việc này bằng cách sử dụng chuỗi chú thích SQL `--` để xóa kiểm tra mật khẩu khỏi `WHERE` mệnh đề truy vấn. Ví dụ: nhập tên người dùng `administrator'--` và mật khẩu trống sẽ dẫn đến truy vấn sau:

`SELECT * FROM users WHERE username = 'administrator'--' AND password = ''`
`username` Truy vấn này trả về tên người dùng `administrator` và đăng nhập thành công vào kẻ tấn công với tư cách là người dùng đó.  
### Phòng thí nghiệm: Lỗ hổng SQL cho phép bỏ qua đăng nhập
[Solution](./lab2.py)  
## Tiêm SQL bậc hai
Tấn công SQL cấp một xảy ra khi ứng dụng xử lý dữ liệu đầu vào của người dùng từ yêu cầu HTTP và kết hợp dữ liệu đầu vào vào truy vấn SQL theo cách không an toàn.  
  
Tiêm SQL bậc hai xảy ra khi ứng dụng lấy dữ liệu đầu vào của người dùng từ một yêu cầu HTTP và lưu trữ để sử dụng trong tương lai. Điều này thường được thực hiện bằng cách đưa dữ liệu đầu vào vào cơ sở dữ liệu, nhưng không có lỗ hổng nào xảy ra tại điểm dữ liệu được lưu trữ. Sau đó, khi xử lý một yêu cầu HTTP khác, ứng dụng sẽ truy xuất dữ liệu đã lưu trữ và kết hợp nó vào một truy vấn SQL theo cách không an toàn. Vì lý do này, tiêm SQL bậc hai còn được gọi là tiêm SQL lưu trữ.  

Tiêm SQL bậc hai thường xảy ra trong trường hợp các nhà phát triển nhận thức được lỗ hổng tiêm SQL và do đó xử lý an toàn việc đưa dữ liệu đầu vào ban đầu vào cơ sở dữ liệu. Khi dữ liệu được xử lý sau đó, nó được coi là an toàn vì trước đó nó đã được đưa vào cơ sở dữ liệu một cách an toàn. Tại thời điểm này, dữ liệu được xử lý theo cách không an toàn vì nhà phát triển đã nhầm lẫn khi cho rằng nó đáng tin cậy.  
## Kiểm tra cơ sở dữ liệu  
Một số tính năng cốt lõi của ngôn ngữ SQL được triển khai theo cùng một cách trên các nền tảng cơ sở dữ liệu phổ biến và rất nhiều cách phát hiện và khai thác lỗ hổng SQL injection hoạt động giống hệt nhau trên các loại cơ sở dữ liệu khác nhau.  
  
Tuy nhiên, cũng có nhiều điểm khác biệt giữa các cơ sở dữ liệu phổ biến. Điều này có nghĩa là một số kỹ thuật phát hiện và khai thác lỗi SQL injection hoạt động khác nhau trên các nền tảng khác nhau. Ví dụ:  
* Cú pháp nối chuỗi.
* Bình luận.
* Truy vấn theo đợt (hoặc xếp chồng).
* API dành riêng cho nền tảng.
* Thông báo lỗi.  

Sau khi xác định được lỗ hổng SQL injection, việc thu thập thông tin về cơ sở dữ liệu thường rất hữu ích. Thông tin này có thể giúp bạn khai thác lỗ hổng.

Bạn có thể truy vấn chi tiết phiên bản của cơ sở dữ liệu. Các phương pháp khác nhau áp dụng cho các loại cơ sở dữ liệu khác nhau. Điều này có nghĩa là nếu bạn tìm thấy một phương pháp cụ thể nào đó hiệu quả, bạn có thể suy ra loại cơ sở dữ liệu. Ví dụ: trên Oracle, bạn có thể thực thi:  
`SELECT * FROM v$version`  

Bạn cũng có thể xác định những bảng cơ sở dữ liệu nào hiện có và các cột chúng chứa. Ví dụ: trên hầu hết các cơ sở dữ liệu, bạn có thể thực hiện truy vấn sau để liệt kê các bảng:  
`SELECT * FROM information_schema.tables`  
## Tiêm SQL trong các bối cảnh khác nhau  
Trong các bài thực hành trước, bạn đã sử dụng chuỗi truy vấn để chèn tải trọng SQL độc hại. Tuy nhiên, bạn có thể thực hiện các cuộc tấn công tiêm nhiễm SQL bằng bất kỳ dữ liệu đầu vào nào có thể kiểm soát được và được ứng dụng xử lý dưới dạng truy vấn SQL. Ví dụ: một số trang web lấy dữ liệu đầu vào ở định dạng JSON hoặc XML và sử dụng chúng để truy vấn cơ sở dữ liệu.  

Những định dạng khác nhau này có thể cung cấp cho bạn nhiều cách khác nhau để che giấu các cuộc tấn công vốn bị chặn nhờ WAF và các cơ chế phòng thủ khác. Các triển khai yếu thường tìm kiếm các từ khóa SQL injection phổ biến trong yêu cầu, vì vậy bạn có thể bỏ qua các bộ lọc này bằng cách mã hóa hoặc thoát các ký tự trong các từ khóa bị cấm. Ví dụ: lệnh SQL injection dựa trên XML sau đây sử dụng chuỗi thoát XML để mã hóa `S` ký tự trong `SELECT`:  
```XML
<stockCheck>
    <productId>123</productId>
    <storeId>999 &#x53;ELECT * FROM information_schema.tables</storeId>
</stockCheck>
```  
Nội dung này sẽ được giải mã ở phía máy chủ trước khi chuyển đến trình thông dịch SQL.  
[SOLUTION](./lab3.py)

## Làm thế nào để ngăn chặn SQL injection
Bạn có thể ngăn chặn hầu hết các trường hợp SQL injection bằng cách sử dụng các truy vấn tham số hóa thay vì nối chuỗi trong truy vấn. Các truy vấn tham số hóa này còn được gọi là "câu lệnh đã chuẩn bị".  
  
Đoạn mã sau đây dễ bị tấn công SQL injection vì dữ liệu đầu vào của người dùng được nối trực tiếp vào truy vấn:  

```
String query = "SELECT * FROM products WHERE category = '"+ input + "'";
Statement statement = connection.createStatement();
ResultSet resultSet = statement.executeQuery(query);
```  
Bạn có thể viết lại mã này theo cách ngăn chặn dữ liệu đầu vào của người dùng can thiệp vào cấu trúc truy vấn:  
```
PreparedStatement statement = connection.prepareStatement("SELECT * FROM products WHERE category = ?");
statement.setString(1, input);
ResultSet resultSet = statement.executeQuery();
``` 
Bạn có thể sử dụng truy vấn tham số hóa cho bất kỳ tình huống nào mà dữ liệu đầu vào không đáng tin cậy xuất hiện dưới dạng dữ liệu trong truy vấn, bao gồm `WHERE` mệnh đề và giá trị trong câu lệnh `INSERT` hoặc `UPDATE`. Chúng không thể được sử dụng để xử lý dữ liệu đầu vào không đáng tin cậy trong các phần khác của truy vấn, chẳng hạn như tên bảng hoặc tên cột, hoặc mệnh `ORDER BY` đề. Chức năng ứng dụng đưa dữ liệu không đáng tin cậy vào các phần này của truy vấn cần áp dụng một cách tiếp cận khác, chẳng hạn như:

Danh sách trắng các giá trị đầu vào được phép.  
Sử dụng logic khác nhau để đưa ra hành vi mong muốn.  
Để một truy vấn tham số hóa có hiệu quả trong việc ngăn chặn tấn công SQL injection, chuỗi được sử dụng trong truy vấn phải luôn là một hằng số được mã hóa cứng. Nó không bao giờ được chứa bất kỳ dữ liệu biến nào từ bất kỳ nguồn gốc nào. Đừng vội vàng quyết định xem một mục dữ liệu có đáng tin cậy hay không theo từng trường hợp, và hãy tiếp tục sử dụng phép nối chuỗi trong truy vấn cho các trường hợp được coi là an toàn. Rất dễ mắc lỗi về nguồn gốc dữ liệu có thể có, hoặc các thay đổi trong mã khác làm ảnh hưởng đến dữ liệu đáng tin cậy.

