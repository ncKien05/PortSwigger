# NoSQL injection  
Lỗ hổng tấn công NoSQL injection cho phép kẻ tấn công can thiệp vào các truy vấn mà ứng dụng thực hiện đối với cơ sở dữ liệu NoSQL. Tấn công NoSQL injection có thể giúp kẻ tấn công:  
* Vượt qua các cơ chế xác thực hoặc bảo vệ.
* Trích xuất hoặc chỉnh sửa dữ liệu.
* Gây ra tình trạng từ chối dịch vụ.
* Thực thi mã trên máy chủ.  

Cơ sở dữ liệu NoSQL lưu trữ và truy xuất dữ liệu ở định dạng khác với các bảng quan hệ SQL truyền thống. Chúng sử dụng nhiều ngôn ngữ truy vấn khác nhau thay vì một tiêu chuẩn chung như SQL, và có ít ràng buộc quan hệ hơn.  

# Các loại tấn công NoSQL injection  
Có hai loại tấn công injection NoSQL khác nhau:  
* Tấn công chèn cú pháp - Điều này xảy ra khi bạn có thể phá vỡ cú pháp truy vấn NoSQL, cho phép bạn chèn mã độc của riêng mình. Phương pháp này tương tự như phương pháp được sử dụng trong tấn công chèn SQL. Tuy nhiên, bản chất của cuộc tấn công khác biệt đáng kể, vì các cơ sở dữ liệu NoSQL sử dụng nhiều ngôn ngữ truy vấn, loại cú pháp truy vấn và cấu trúc dữ liệu khác nhau.  
* Chèn toán tử - Điều này xảy ra khi bạn có thể sử dụng các toán tử truy vấn NoSQL để thao tác các truy vấn.  

Trong chủ đề này, chúng ta sẽ xem xét cách kiểm tra các lỗ hổng NoSQL nói chung, sau đó tập trung vào việc khai thác các lỗ hổng trong MongoDB, cơ sở dữ liệu NoSQL phổ biến nhất. Chúng tôi cũng đã cung cấp một số bài thực hành để bạn có thể thực hành những gì đã học.  

# Tiêm cú pháp NoSQL  

Bạn có thể phát hiện các lỗ hổng tấn công injection NoSQL bằng cách cố gắng phá vỡ cú pháp truy vấn. Để làm điều này, hãy kiểm tra từng dữ liệu đầu vào một cách có hệ thống bằng cách gửi các chuỗi giả lập và các ký tự đặc biệt gây ra lỗi cơ sở dữ liệu hoặc một số hành vi có thể phát hiện được khác nếu chúng không được ứng dụng xử lý hoặc lọc đúng cách.  

Nếu bạn biết ngôn ngữ API của cơ sở dữ liệu mục tiêu, hãy sử dụng các ký tự đặc biệt và chuỗi lỗi phù hợp với ngôn ngữ đó. Nếu không, hãy sử dụng nhiều chuỗi lỗi khác nhau để nhắm mục tiêu vào nhiều ngôn ngữ API.  

## Phát hiện tấn công chèn cú pháp trong MongoDB  
Hãy xem xét một ứng dụng mua sắm hiển thị các sản phẩm thuộc nhiều danh mục khác nhau. Khi người dùng chọn danh mục Đồ uống có ga , trình duyệt của họ sẽ yêu cầu URL sau:  
`https://insecure-website.com/product/lookup?category=fizzy`  
Điều này khiến ứng dụng gửi một truy vấn JSON để lấy các sản phẩm liên quan từ bộ productsưu tập trong cơ sở dữ liệu MongoDB:  
`this.category == 'fizzy'`  
Để kiểm tra xem dữ liệu đầu vào có dễ bị tấn công hay không, hãy nhập một chuỗi kiểm thử (fuzz string) vào giá trị của `category`tham số. Ví dụ về chuỗi kiểm thử cho MongoDB là:  
```
'"`{
;$Foo}
$Foo \xYZ
```
Sử dụng chuỗi mã gây nhiễu này để xây dựng cuộc tấn công sau:  
`https://insecure-website.com/product/lookup?category='%22%60%7b%0d%0a%3b%24Foo%7d%0d%0a%24Foo%20%5cxYZ%00`  
Nếu điều này gây ra sự thay đổi so với phản hồi ban đầu, điều đó có thể cho thấy dữ liệu người dùng nhập vào chưa được lọc hoặc xử lý đúng cách.  


**Ghi chú**  
Lỗ hổng tấn công injection NoSQL có thể xảy ra trong nhiều ngữ cảnh khác nhau, và bạn cần điều chỉnh chuỗi kiểm thử (fuzz strings) cho phù hợp. Nếu không, bạn có thể chỉ gây ra lỗi xác thực dẫn đến việc ứng dụng không bao giờ thực thi truy vấn của bạn.

Trong ví dụ này, chúng ta chèn chuỗi kiểm thử thông qua URL, vì vậy chuỗi được mã hóa URL. Trong một số ứng dụng, bạn có thể cần chèn dữ liệu thông qua thuộc tính JSON. Trong trường hợp này, dữ liệu sẽ trở thành ```'\"`{\r;$Foo}\n$Foo \\xYZ\u0000```.  

### Xác định các ký tự nào được xử lý  
Để xác định ký tự nào được ứng dụng hiểu là cú pháp, bạn có thể chèn từng ký tự riêng lẻ. Ví dụ, bạn có thể gửi `'`, dẫn đến truy vấn MongoDB sau:  
`this.category == '''`  
Nếu điều này gây ra sự thay đổi so với phản hồi ban đầu, điều đó có thể cho thấy 'ký tự đó đã phá vỡ cú pháp truy vấn và gây ra lỗi cú pháp. Bạn có thể xác nhận điều này bằng cách gửi một chuỗi truy vấn hợp lệ vào ô nhập liệu, ví dụ bằng cách thoát dấu ngoặc kép:  
`this.category == '\''`  
Nếu điều này không gây ra lỗi cú pháp, điều đó có thể có nghĩa là ứng dụng dễ bị tấn công bằng phương pháp chèn mã độc.  

### Xác nhận hành vi có điều kiện  
Sau khi phát hiện ra lỗ hổng, bước tiếp theo là xác định xem bạn có thể tác động đến các điều kiện boolean bằng cú pháp NoSQL hay không.

Để kiểm tra điều này, hãy gửi hai yêu cầu, một yêu cầu với điều kiện sai và một yêu cầu với điều kiện đúng. Ví dụ, bạn có thể sử dụng các câu lệnh điều kiện `' && 0 && 'x` và `' && 1 && 'x` như sau:

`https://insecure-website.com/product/lookup?category=fizzy'+%26%26+0+%26%26+'x`  
`https://insecure-website.com/product/lookup?category=fizzy'+%26%26+1+%26%26+'x`  
Nếu ứng dụng hoạt động khác đi, điều này cho thấy điều kiện sai ảnh hưởng đến logic truy vấn, nhưng điều kiện đúng thì không. Điều này chỉ ra rằng việc chèn kiểu cú pháp này ảnh hưởng đến truy vấn phía máy chủ.  

### Ghi đè lên các điều kiện hiện có  
Giờ đây, khi bạn đã nhận ra rằng mình có thể tác động đến các điều kiện boolean, bạn có thể thử ghi đè các điều kiện hiện có để khai thác lỗ hổng. Ví dụ, bạn có thể chèn một điều kiện JavaScript luôn luôn đúng, chẳng hạn như `'||'1'=='1`:  
`https://insecure-website.com/product/lookup?category=fizzy%27%7c%7c%27%31%27%3d%3d%27%31`  
Điều này dẫn đến truy vấn MongoDB sau:  
`this.category == 'fizzy'||'1'=='1'`  
Vì điều kiện được chèn luôn đúng, truy vấn đã sửa đổi sẽ trả về tất cả các mục. Điều này cho phép bạn xem tất cả các sản phẩm trong bất kỳ danh mục nào, bao gồm cả các danh mục ẩn hoặc không xác định.  

**Cảnh báo**  
Cần thận trọng khi chèn điều kiện luôn đúng vào truy vấn NoSQL. Mặc dù điều này có vẻ vô hại trong ngữ cảnh ban đầu bạn chèn vào, nhưng các ứng dụng thường sử dụng dữ liệu từ một yêu cầu duy nhất trong nhiều truy vấn khác nhau. Nếu ứng dụng sử dụng nó khi cập nhật hoặc xóa dữ liệu, chẳng hạn, điều này có thể dẫn đến mất dữ liệu ngoài ý muốn.  

#### Bài thực hành: Phát hiện tấn công injection NoSQL  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/NoSql_Injection/Solution/lab1.py)  

Bạn cũng có thể thêm ký tự null sau giá trị danh mục. MongoDB có thể bỏ qua tất cả các ký tự sau ký tự null. Điều này có nghĩa là bất kỳ điều kiện bổ sung nào trong truy vấn MongoDB đều bị bỏ qua. Ví dụ, truy vấn có thể có thêm một `this.released` ràng buộc:

`this.category == 'fizzy' && this.released == 1`  
Hạn chế này `this.released == 1` được sử dụng để chỉ hiển thị các sản phẩm đã được phát hành. Đối với các sản phẩm chưa phát hành, có lẽ `this.released == 0`...

Trong trường hợp này, kẻ tấn công có thể xây dựng một cuộc tấn công như sau:

`https://insecure-website.com/product/lookup?category=fizzy'%00`  
Điều này dẫn đến truy vấn NoSQL sau:

`this.category == 'fizzy'\u0000' && this.released == 1`  
Nếu MongoDB bỏ qua tất cả các ký tự sau ký tự null, điều này sẽ loại bỏ yêu cầu trường "released" phải được đặt thành 1. Kết quả là, tất cả các sản phẩm trong danh fizzymục đều được hiển thị, bao gồm cả các sản phẩm chưa được phát hành.  

## Tấn công chèn toán tử NoSQL  

Các cơ sở dữ liệu NoSQL thường sử dụng các toán tử truy vấn, cung cấp các cách để chỉ định các điều kiện mà dữ liệu phải đáp ứng để được đưa vào kết quả truy vấn. Ví dụ về các toán tử truy vấn MongoDB bao gồm:

* `$where` - Tìm các tài liệu thỏa mãn biểu thức JavaScript.
* `$ne` - Khớp với tất cả các giá trị không bằng một giá trị được chỉ định.
* `$in` - Khớp với tất cả các giá trị được chỉ định trong một mảng.
* `$regex` - Chọn các tài liệu có giá trị khớp với biểu thức chính quy được chỉ định.  

Bạn có thể chèn các toán tử truy vấn để thao tác với các truy vấn NoSQL. Để làm điều này, hãy nhập các toán tử khác nhau vào nhiều ô nhập liệu của người dùng một cách có hệ thống, sau đó xem xét các phản hồi để tìm thông báo lỗi hoặc các thay đổi khác.
  
### Toán tử gửi truy vấn  
Trong các thông báo JSON, bạn có thể chèn các toán tử truy vấn dưới dạng các đối tượng lồng nhau. Ví dụ: `{"username":"wiener"}` trở thành `{"username":{"$ne":"invalid"}}`.

Đối với các đầu vào dựa trên URL, bạn có thể chèn các toán tử truy vấn thông qua các tham số URL. Ví dụ: `username=wiener` trở thành `username[$ne]=invalid`. Nếu cách này không hiệu quả, bạn có thể thử cách sau:  

* Chuyển đổi phương thức yêu cầu từ `GET` sang `POST`.  
* Thay đổi `Content-Type` tiêu đề thành `application/json`.  
* Thêm JSON vào nội dung tin nhắn.  
* Chèn các toán tử truy vấn vào JSON.  

**Ghi chú**  
Bạn có thể sử dụng tiện ích mở rộng Content Type Converter để tự động chuyển đổi phương thức yêu cầu và thay đổi yêu cầu được mã hóa URL `POST` thành JSON.  

### Phát hiện tấn công chèn toán tử trong MongoDB  
Hãy xem xét một ứng dụng dễ bị tấn công chấp nhận tên người dùng và mật khẩu trong phần thân của `POST` yêu cầu:  

`{"username":"wiener","password":"peter"}`  

Kiểm tra từng đầu vào với một loạt các toán tử. Ví dụ, để kiểm tra xem đầu vào tên người dùng có xử lý toán tử truy vấn hay không, bạn có thể thử phương pháp tấn công chèn sau:  

`{"username":{"$ne":"invalid"},"password":"peter"}`  

Nếu `$ne` toán tử này được áp dụng, nó sẽ truy vấn tất cả người dùng có tên người dùng khác với `invalid`.  

Nếu cả tên người dùng và mật khẩu đều được người dùng nhập vào, có thể sẽ vượt qua được quá trình xác thực bằng cách sử dụng đoạn mã sau:  

`{"username":{"$ne":"invalid"},"password":{"$ne":"invalid"}}`  

Truy vấn này trả về tất cả thông tin đăng nhập mà cả tên người dùng và mật khẩu đều không bằng nhau `invalid`. Kết quả là, bạn được đăng nhập vào ứng dụng với tư cách người dùng đầu tiên trong tập hợp.  

Để nhắm mục tiêu vào một tài khoản, bạn có thể tạo một payload bao gồm tên người dùng đã biết hoặc tên người dùng mà bạn đã đoán được. Ví dụ:  

`{"username":{"$in":["admin","administrator","superadmin"]},"password":{"$ne":""}}`  

#### Bài thực hành: Khai thác lỗ hổng tấn công chèn toán tử NoSQL để vượt qua xác thực.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/NoSql_Injection/Solution/lab2.py)  

# Khai thác lỗ hổng tấn công chèn cú pháp để trích xuất dữ liệu  
Trong nhiều cơ sở dữ liệu NoSQL, một số toán tử hoặc hàm truy vấn có thể chạy mã JavaScript giới hạn, chẳng hạn như `$where` toán tử và `mapReduce()` hàm của MongoDB. Điều này có nghĩa là, nếu một ứng dụng dễ bị tổn thương sử dụng các toán tử hoặc hàm này, cơ sở dữ liệu có thể đánh giá JavaScript như một phần của truy vấn. Do đó, bạn có thể sử dụng các hàm JavaScript để trích xuất dữ liệu từ cơ sở dữ liệu.  

## Trích xuất dữ liệu trong MongoDB  
Hãy xem xét một ứng dụng dễ bị tấn công cho phép người dùng tra cứu tên người dùng đã đăng ký khác và hiển thị vai trò của họ. Điều này kích hoạt yêu cầu đến URL:

`https://insecure-website.com/user/lookup?username=admin`  
Điều này dẫn đến truy vấn NoSQL sau đây đối với `users` tập hợp dữ liệu:

`{" $where":"this.username == 'admin'"}`  
Vì truy vấn sử dụng `$where` toán tử, bạn có thể cố gắng chèn các hàm JavaScript vào truy vấn này để nó trả về dữ liệu nhạy cảm. Ví dụ, bạn có thể gửi tải trọng sau:  

`admin' && this.password[0] == 'a' || 'a'=='b`  
Thao tác này trả về ký tự đầu tiên của chuỗi mật khẩu người dùng, cho phép bạn trích xuất mật khẩu từng ký tự một.

Bạn cũng có thể sử dụng `match()` hàm JavaScript để trích xuất thông tin. Ví dụ, đoạn mã sau cho phép bạn xác định xem mật khẩu có chứa chữ số hay không:

`admin' && this.password.match(/\d/) || 'a'=='b`  

#### Bài thực hành: Khai thác lỗ hổng tấn công NoSQL injection để trích xuất dữ liệu  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/NoSql_Injection/Solution/lab3.py)  

### Xác định tên trường  
Vì MongoDB xử lý dữ liệu bán cấu trúc không yêu cầu lược đồ cố định, bạn có thể cần xác định các trường hợp lệ trong tập hợp dữ liệu trước khi có thể trích xuất dữ liệu bằng cách sử dụng phương pháp chèn JavaScript.

Ví dụ, để xác định xem cơ sở dữ liệu MongoDB có chứa một `password` trường cụ thể hay không, bạn có thể gửi dữ liệu như sau:

`https://insecure-website.com/user/lookup?username=admin'+%26%26+this.password!%3d'`  
Gửi lại dữ liệu cho trường đã tồn tại và cho trường chưa tồn tại. Trong ví dụ này, bạn biết rằng `username` trường đó tồn tại, vì vậy bạn có thể gửi các dữ liệu sau:  

`admin' && this.username!='`  
`admin' && this.foo!='`  
Nếu `password` trường tồn tại, bạn sẽ mong đợi phản hồi giống hệt với phản hồi cho trường hiện có (`username`), nhưng khác với phản hồi cho trường không tồn tại (`foo`).

Nếu bạn muốn kiểm tra các tên trường khác nhau, bạn có thể thực hiện tấn công bằng từ điển, bằng cách sử dụng danh sách từ để duyệt qua các tên trường tiềm năng khác nhau.  

**Ghi chú**  
Ngoài ra, bạn cũng có thể sử dụng phương pháp tấn công chèn toán tử NoSQL để trích xuất tên trường từng ký tự một. Điều này cho phép bạn xác định tên trường mà không cần phải đoán hoặc thực hiện tấn công từ điển. Chúng tôi sẽ hướng dẫn bạn cách thực hiện điều này trong phần tiếp theo.

# Khai thác lỗ hổng tấn công chèn toán tử NoSQL để trích xuất dữ liệu  
Ngay cả khi truy vấn gốc không sử dụng bất kỳ toán tử nào cho phép bạn chạy JavaScript tùy ý, bạn vẫn có thể tự chèn một trong những toán tử này. Sau đó, bạn có thể sử dụng các điều kiện boolean để xác định xem ứng dụng có thực thi bất kỳ JavaScript nào mà bạn chèn thông qua toán tử này hay không.  
## Chèn toán tử vào MongoDB
Hãy xem xét một ứng dụng dễ bị tấn công chấp nhận tên người dùng và mật khẩu trong phần thân của `POST` yêu cầu:

`{"username":"wiener","password":"peter"}`  

Để kiểm tra xem bạn có thể chèn toán tử hay không, bạn có thể thử thêm toán `$where` tử như một tham số bổ sung, sau đó gửi một yêu cầu trong đó điều kiện được đánh giá là sai và một yêu cầu khác đánh giá là đúng. Ví dụ:

`{"username":"wiener","password":"peter", "$where":"0"}`  
`{"username":"wiener","password":"peter", "$where":"1"}`  

Nếu có sự khác biệt giữa các phản hồi, điều này có thể cho thấy biểu thức JavaScript trong mệnh `$where` đề đang được đánh giá.  

### Trích xuất tên trường  
Nếu bạn đã chèn một toán tử cho phép bạn chạy JavaScript, bạn có thể sử dụng `keys()` phương thức này để trích xuất tên của các trường dữ liệu. Ví dụ, bạn có thể gửi dữ liệu sau:

`"$where":"Object.keys(this)[0].match('^.{0}a.*')"`  

Thao tác này kiểm tra trường dữ liệu đầu tiên trong đối tượng người dùng và trả về ký tự đầu tiên của tên trường. Điều này cho phép bạn trích xuất tên trường từng ký tự một.  

#### Bài thực hành: Khai thác lỗ hổng tấn công chèn toán tử NoSQL để trích xuất các trường chưa biết  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/NoSql_Injection/Solution/lab4.py)  

### Trích xuất dữ liệu bằng cách sử dụng toán tử  

Ngoài ra, bạn cũng có thể trích xuất dữ liệu bằng cách sử dụng các toán tử không cho phép chạy JavaScript. Ví dụ, bạn có thể sử dụng toán `$regex` tử để trích xuất dữ liệu từng ký tự một.

Hãy xem xét một ứng dụng dễ bị tấn công chấp nhận tên người dùng và mật khẩu trong phần thân của `POST` yêu cầu. Ví dụ:

`{"username":"myuser","password":"mypass"}`  

Bạn có thể bắt đầu bằng cách kiểm tra xem `$regex` toán tử có được xử lý như sau hay không:

`{"username":"admin","password":{"$regex":"^.*"}}`  

Nếu phản hồi cho yêu cầu này khác với phản hồi bạn nhận được khi nhập mật khẩu không chính xác, điều này cho thấy ứng dụng có thể dễ bị tấn công. Bạn có thể sử dụng toán `$regex` tử để trích xuất dữ liệu từng ký tự một. Ví dụ, đoạn mã sau kiểm tra xem mật khẩu có bắt đầu bằng dấu hai chấm (:) hay không `a`.

`{"username":"admin","password":{"$regex":"^a*"}}`  

## Tiêm theo thời gian  
Đôi khi việc gây ra lỗi cơ sở dữ liệu không làm thay đổi phản hồi của ứng dụng. Trong trường hợp này, bạn vẫn có thể phát hiện và khai thác lỗ hổng bằng cách sử dụng kỹ thuật chèn JavaScript để kích hoạt độ trễ thời gian có điều kiện.

Để thực hiện tấn công injection NoSQL dựa trên thời gian:

Hãy tải trang nhiều lần để xác định thời gian tải cơ bản.
Chèn một payload dựa trên thời gian vào đầu vào. Payload dựa trên thời gian sẽ gây ra sự chậm trễ có chủ ý trong phản hồi khi được thực thi. Ví dụ, `{"$where": "sleep(5000)"}` gây ra sự chậm trễ có chủ ý là 5000 ms khi chèn thành công.
Xác định xem phản hồi có tải chậm hơn không. Điều này cho thấy quá trình tiêm thành công.
Các đoạn mã xử lý dữ liệu dựa trên thời gian sau đây sẽ kích hoạt độ trễ thời gian nếu mật khẩu bắt đầu bằng chữ cái `a`:  

`admin'+function(x){var waitTill = new Date(new Date().getTime() + 5000);while((x.password[0]==="a") && waitTill > new Date()){};}(this)+'`  

`admin'+function(x){if(x.password[0]==="a"){sleep(5000)};}(this)+'`  

# Ngăn chặn tấn công NoSQL injection  
Cách thức phù hợp để ngăn chặn các cuộc tấn công injection vào NoSQL phụ thuộc vào công nghệ NoSQL cụ thể đang được sử dụng. Do đó, chúng tôi khuyên bạn nên đọc tài liệu bảo mật của cơ sở dữ liệu NoSQL mà bạn lựa chọn. Tuy nhiên, các hướng dẫn chung sau đây cũng sẽ hữu ích:  

* Lọc và xác thực dữ liệu nhập của người dùng, sử dụng danh sách các ký tự được chấp nhận.  
* Chèn dữ liệu do người dùng nhập bằng cách sử dụng các truy vấn tham số hóa thay vì nối trực tiếp dữ liệu do người dùng nhập vào truy vấn.  
* Để ngăn chặn tấn công chèn mã độc, hãy áp dụng danh sách cho phép các khóa được chấp nhận.  