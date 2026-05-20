# Ngữ cảnh tấn công kịch bản chéo trang  
Khi kiểm tra các lỗ hổng XSS phản chiếu và lưu trữ , một nhiệm vụ quan trọng là xác định ngữ cảnh của lỗ hổng XSS:

* Vị trí trong phản hồi nơi dữ liệu do kẻ tấn công kiểm soát xuất hiện.
* Bất kỳ quá trình xác thực dữ liệu đầu vào hoặc xử lý nào khác mà ứng dụng đang thực hiện trên dữ liệu đó.  

Dựa trên những thông tin chi tiết này, bạn có thể chọn một hoặc nhiều payload XSS tiềm năng và kiểm tra xem chúng có hiệu quả hay không.  

# Lỗ hổng XSS giữa các thẻ HTML  
Khi ngữ cảnh XSS là văn bản nằm giữa các thẻ HTML, bạn cần thêm một số thẻ HTML mới được thiết kế để kích hoạt việc thực thi JavaScript.

Một số cách hữu ích để thực thi JavaScript là:  

```javascript
<script>alert(document.domain)</script>
<img src=1 onerror=alert(1)>
```

### Thực hành: Phản chiếu lỗ hổng XSS vào ngữ cảnh HTML với hầu hết các thẻ và thuộc tính bị chặn.
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Solution/lab11.py)

### Thực hành: Phản chiếu lỗ hổng XSS vào ngữ cảnh HTML với tất cả các thẻ bị chặn ngoại trừ các thẻ tùy chỉnh.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Solution/lab12.py)

### Bài thực hành: Tấn công XSS phản chiếu với trình xử lý sự kiện và thuộc tính href bị chặn  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Solution/lab13.py)

### Thực hành: Tấn công XSS phản chiếu với một số mã đánh dấu SVG được cho phép.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Solution/lab14.py)

# Lỗ hổng XSS trong thuộc tính thẻ HTML  
Khi lỗi XSS xảy ra trong giá trị thuộc tính của thẻ HTML, đôi khi bạn có thể kết thúc giá trị thuộc tính đó, đóng thẻ và thêm một giá trị mới. Ví dụ:  

`"><script>alert(document.domain)</script>`  

Thông thường trong trường hợp này, dấu ngoặc nhọn bị chặn hoặc mã hóa, do đó dữ liệu nhập của bạn không thể thoát ra khỏi thẻ chứa nó. Miễn là bạn có thể kết thúc giá trị thuộc tính, bạn thường có thể thêm một thuộc tính mới tạo ra ngữ cảnh có thể lập trình được, chẳng hạn như trình xử lý sự kiện. Ví dụ:  

`" autofocus onfocus=alert(document.domain) x="`

Đoạn mã trên tạo ra một `onfocus` sự kiện sẽ thực thi JavaScript khi phần tử nhận được tiêu điểm, đồng thời thêm `autofocus` thuộc tính để cố gắng kích hoạt `onfocus` sự kiện tự động mà không cần bất kỳ tương tác nào của người dùng. Cuối cùng, nó bổ sung chức `x="` năng sửa chữa khéo léo cho đoạn mã đánh dấu tiếp theo.  

### Bài thực hành: Tấn công XSS phản chiếu vào thuộc tính có dấu ngoặc nhọn được mã hóa HTML.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Solution/lab15.py)  

Đôi khi, ngữ cảnh XSS nằm trong một loại thuộc tính thẻ HTML mà bản thân thuộc tính đó có thể tạo ra ngữ cảnh có thể thực thi bằng script. Tại đây, bạn có thể thực thi JavaScript mà không cần phải kết thúc giá trị thuộc tính. Ví dụ, nếu ngữ cảnh XSS nằm trong thuộc `href`tính của thẻ neo (anchor tag), bạn có thể sử dụng giao `javascript`thức giả (pseudo-protocol) để thực thi script. Ví dụ:  

`<a href="javascript:alert(document.domain)">`  

### Bài thực hành: Lỗ hổng XSS được lưu trữ trong thuộc tính liên kết `href` có dấu ngoặc kép được mã hóa HTML.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Solution/lab16.py)  

Bạn có thể gặp phải các trang web mã hóa dấu ngoặc nhọn nhưng vẫn cho phép bạn chèn thuộc tính. Đôi khi, việc chèn này có thể thực hiện được ngay cả trong các thẻ thường không tự động kích hoạt sự kiện, chẳng hạn như thẻ `canonical`. Bạn có thể khai thác hành vi này bằng cách sử dụng phím tắt và tương tác người dùng trên Chrome. Phím tắt cho phép bạn cung cấp các phím tắt bàn phím tham chiếu đến một phần tử cụ thể. Thuộc tính `accesskey` cho phép bạn xác định một chữ cái mà khi được nhấn kết hợp với các phím khác (các phím này khác nhau trên các nền tảng khác nhau), sẽ kích hoạt các sự kiện. Trong bài thực hành tiếp theo, bạn có thể thử nghiệm với phím tắt và khai thác thẻ `canonical`.  

### Bài thực hành: Tấn công XSS phản chiếu trong thẻ liên kết chuẩn  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Solution/lab17.py)

# Lỗ hổng XSS trong JavaScript  
Khi ngữ cảnh XSS là một đoạn mã JavaScript hiện có trong phản hồi, nhiều tình huống khác nhau có thể phát sinh, đòi hỏi các kỹ thuật khác nhau để thực hiện thành công cuộc tấn công. 

## Chấm dứt kịch bản hiện có  
Trong trường hợp đơn giản nhất, có thể chỉ cần đóng thẻ `<script>` bao quanh đoạn mã JavaScript hiện có và thêm một số thẻ HTML mới để kích hoạt việc thực thi JavaScript. Ví dụ, nếu ngữ cảnh XSS như sau:

```javascript
<script>
...
var input = 'controllable data here';
...
</script>
```  

Sau đó, bạn có thể sử dụng đoạn mã sau để thoát khỏi mã JavaScript hiện có và thực thi mã của riêng mình:  
`</script><img src=1 onerror=alert(document.domain)>`  

Lý do điều này hoạt động là vì trình duyệt trước tiên thực hiện phân tích cú pháp HTML để xác định các phần tử trang bao gồm các khối mã lệnh, và chỉ sau đó mới thực hiện phân tích cú pháp JavaScript để hiểu và thực thi các mã lệnh được nhúng. Đoạn mã trên làm hỏng mã lệnh gốc, với một chuỗi ký tự chưa được kết thúc. Nhưng điều đó không ngăn cản mã lệnh tiếp theo được phân tích cú pháp và thực thi theo cách thông thường.  

### Bài thực hành: Tấn công XSS phản chiếu vào chuỗi JavaScript với dấu ngoặc đơn và dấu gạch chéo ngược được thoát.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Solution/lab18.py)

## Thoát khỏi chuỗi JavaScript  
Trong trường hợp ngữ cảnh XSS nằm bên trong một chuỗi ký tự được trích dẫn, thường có thể thoát khỏi chuỗi và thực thi JavaScript trực tiếp. Điều cần thiết là phải sửa chữa kịch bản sau ngữ cảnh XSS, vì bất kỳ lỗi cú pháp nào ở đó sẽ ngăn toàn bộ kịch bản được thực thi.

Một số cách hữu ích để thoát khỏi chuỗi ký tự cố định là:  
```
'-alert(document.domain)-'
';alert(document.domain)//
```

### Bài thực hành: Tấn công XSS phản chiếu vào chuỗi JavaScript có chứa dấu ngoặc nhọn được mã hóa HTML.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Solution/lab19.py)

Một số ứng dụng cố gắng ngăn chặn việc nhập liệu thoát khỏi chuỗi JavaScript bằng cách mã hóa bất kỳ ký tự dấu ngoặc đơn nào bằng dấu gạch chéo ngược. Dấu gạch chéo ngược trước một ký tự báo cho trình phân tích cú pháp JavaScript biết rằng ký tự đó nên được hiểu theo nghĩa đen, chứ không phải là một ký tự đặc biệt như ký tự kết thúc chuỗi. Trong trường hợp này, các ứng dụng thường mắc lỗi không mã hóa chính ký tự dấu gạch chéo ngược. Điều này có nghĩa là kẻ tấn công có thể sử dụng ký tự dấu gạch chéo ngược của riêng chúng để vô hiệu hóa dấu gạch chéo ngược do ứng dụng thêm vào.

Ví dụ, giả sử đầu vào là:  

`';alert(document.domain)//`  
Được chuyển đổi thành:  

`\';alert(document.domain)//`  

Giờ bạn có thể sử dụng tải trọng thay thế:

`\';alert(document.domain)//`

Dữ liệu nhập được mã hóa thành:  

`\\';alert(document.domain)//`  

Ở đây, dấu gạch chéo ngược đầu tiên có nghĩa là dấu gạch chéo ngược thứ hai được hiểu theo nghĩa đen, chứ không phải là một ký tự đặc biệt. Điều này có nghĩa là dấu ngoặc kép giờ được hiểu là ký tự kết thúc chuỗi, và do đó cuộc tấn công thành công.  

### Bài thực hành: Tấn công XSS phản chiếu vào chuỗi JavaScript có chứa dấu ngoặc nhọn và dấu ngoặc kép được mã hóa HTML và dấu ngoặc đơn được thoát.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Solution/lab20.py)  

Một số trang web làm cho việc tấn công XSS trở nên khó khăn hơn bằng cách hạn chế các ký tự bạn được phép sử dụng. Điều này có thể được thực hiện ở cấp độ trang web hoặc bằng cách triển khai tường lửa ứng dụng web (WAF) ngăn chặn các yêu cầu của bạn đến được trang web. Trong những trường hợp này, bạn cần thử nghiệm các cách khác để gọi các hàm nhằm vượt qua các biện pháp bảo mật này. Một cách để làm điều này là sử dụng câu lệnh `throw` với trình xử lý ngoại lệ. Điều này cho phép bạn truyền các đối số cho một hàm mà không cần sử dụng dấu ngoặc đơn. Đoạn mã sau gán hàm `alert()` cho trình xử lý ngoại lệ toàn cục và câu lệnh `throw` truyền đối số `1` cho  trình xử lý ngoại lệ (trong trường hợp này là `alert`). Kết quả cuối cùng là hàm `alert()` được gọi với đối số là `1` .

`onerror=alert;throw 1`  

Bài thực hành tiếp theo sẽ giới thiệu một trang web lọc các ký tự nhất định. Bạn sẽ phải sử dụng các kỹ thuật tương tự như đã mô tả ở trên để giải quyết bài toán này.

### Bài thực hành: Tấn công XSS phản xạ trong URL JavaScript có một số ký tự bị chặn  
[Not Solved](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/Solution/lab21.py)  