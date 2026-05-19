# Tấn công kịch bản chéo trang dựa trên DOM là gì?  
Các lỗ hổng XSS dựa trên DOM thường phát sinh khi JavaScript lấy dữ liệu từ một nguồn do kẻ tấn công kiểm soát, chẳng hạn như URL, và chuyển nó đến một đích hỗ trợ thực thi mã động, chẳng hạn như `eval()` hoặc `innerHTML`. Điều này cho phép kẻ tấn công thực thi JavaScript độc hại, thường cho phép chúng chiếm đoạt tài khoản của người dùng khác.

Để thực hiện một cuộc tấn công XSS dựa trên DOM, bạn cần đưa dữ liệu vào nguồn sao cho nó được truyền đến đích và gây ra việc thực thi mã JavaScript tùy ý.

Nguồn gốc phổ biến nhất của lỗ hổng DOM XSS là URL, thường được truy cập bằng đối tượng `window.location`. Kẻ tấn công có thể tạo một liên kết để dẫn nạn nhân đến một trang dễ bị tổn thương với mã độc trong chuỗi truy vấn và các phần bị phân mảnh của URL. Trong một số trường hợp, chẳng hạn như khi nhắm mục tiêu vào trang 404 hoặc một trang web chạy PHP, mã độc cũng có thể được đặt trong đường dẫn.  

# Cách kiểm tra lỗi tấn công kịch bản chéo trang dựa trên DOM  
Hầu hết các lỗ hổng XSS DOM có thể được phát hiện nhanh chóng và đáng tin cậy bằng cách sử dụng trình quét lỗ hổng web của Burp Suite. Để kiểm tra thủ công các lỗ hổng XSS dựa trên DOM, bạn thường cần sử dụng trình duyệt có công cụ dành cho nhà phát triển, chẳng hạn như Chrome. Bạn cần lần lượt xem xét từng nguồn có sẵn và kiểm tra từng nguồn một cách riêng lẻ.  

## Kiểm tra các bộ lọc HTML  
Để kiểm tra lỗ hổng DOM XSS trong một mã HTML đích, hãy chèn một chuỗi ký tự chữ và số ngẫu nhiên vào mã nguồn (ví dụ: `location.search`), sau đó sử dụng công cụ dành cho nhà phát triển để kiểm tra HTML và tìm vị trí xuất hiện của chuỗi đó. Lưu ý rằng tùy chọn "Xem mã nguồn" của trình duyệt sẽ không hoạt động đối với việc kiểm tra DOM XSS vì nó không tính đến các thay đổi đã được thực hiện trong HTML bởi JavaScript. Trong công cụ dành cho nhà phát triển của Chrome, bạn có thể sử dụng `Ctrl+F` (hoặc `Command+F` trên MacOS) để tìm kiếm chuỗi của mình trong DOM.

Đối với mỗi vị trí mà chuỗi của bạn xuất hiện trong DOM, bạn cần xác định ngữ cảnh. Dựa trên ngữ cảnh này, bạn cần tinh chỉnh đầu vào của mình để xem nó được xử lý như thế nào. Ví dụ, nếu chuỗi của bạn xuất hiện trong một thuộc tính được đặt trong dấu ngoặc kép, hãy thử chèn dấu ngoặc kép vào chuỗi của bạn để xem liệu bạn có thể thoát khỏi thuộc tính đó hay không.

Lưu ý rằng các trình duyệt có cách xử lý mã hóa URL khác nhau. Chrome, Firefox và Safari sẽ mã hóa URL `location.search`, `location.hash` trong khi IE11 và Microsoft Edge (phiên bản trước Chromium) sẽ không mã hóa URL các nguồn này. Nếu dữ liệu của bạn được mã hóa URL trước khi xử lý, thì cuộc tấn công XSS khó có thể thành công.  

## Kiểm tra các điểm thực thi JavaScript  

Kiểm tra các sink thực thi JavaScript để tìm lỗ hổng XSS dựa trên DOM sẽ khó hơn một chút. Với các sink này, dữ liệu đầu vào của bạn không nhất thiết phải xuất hiện ở bất kỳ đâu trong DOM, vì vậy bạn không thể tìm kiếm nó. Thay vào đó, bạn cần sử dụng trình gỡ lỗi JavaScript để xác định xem dữ liệu đầu vào của bạn có được gửi đến sink hay không và bằng cách nào.

Đối với mỗi nguồn tiềm năng, chẳng hạn như location, trước tiên bạn cần tìm các trường hợp trong mã JavaScript của trang nơi nguồn đó được tham chiếu. Trong công cụ dành cho nhà phát triển của Chrome, bạn có thể sử dụng `Control+Shift+F` (hoặc `Command+Alt+F` trên MacOS) để tìm kiếm toàn bộ mã JavaScript của trang nhằm tìm nguồn đó.

Khi đã tìm thấy nơi nguồn dữ liệu được đọc, bạn có thể sử dụng trình gỡ lỗi JavaScript để thêm điểm dừng và theo dõi cách giá trị của nguồn được sử dụng. Bạn có thể thấy rằng nguồn được gán cho các biến khác. Nếu vậy, bạn cần sử dụng lại chức năng tìm kiếm để theo dõi các biến này và xem liệu chúng có được truyền đến một sink hay không. Khi tìm thấy một sink đang nhận dữ liệu có nguồn gốc từ nguồn, bạn có thể sử dụng trình gỡ lỗi để kiểm tra giá trị bằng cách di chuột qua biến để hiển thị giá trị của nó trước khi được gửi đến sink. Sau đó, tương tự như với các sink HTML, bạn cần tinh chỉnh đầu vào của mình để xem liệu bạn có thể thực hiện thành công một cuộc tấn công XSS hay không.

## Kiểm tra lỗ hổng DOM XSS bằng DOM Invader  

Việc xác định và khai thác lỗ hổng DOM XSS trong thực tế có thể là một quá trình tốn nhiều thời gian, thường yêu cầu bạn phải tự tay rà soát các đoạn mã JavaScript phức tạp đã được thu nhỏ. Tuy nhiên, nếu bạn sử dụng trình duyệt của Burp, bạn có thể tận dụng tiện ích mở rộng DOM Invader tích hợp sẵn, tiện ích này sẽ giúp bạn thực hiện phần lớn công việc khó khăn đó.  

# Khai thác lỗ hổng DOM XSS với nhiều nguồn và đích khác nhau  
Về nguyên tắc, một trang web dễ bị tấn công kịch bản chéo trang dựa trên DOM nếu có một đường dẫn thực thi mà qua đó dữ liệu có thể lan truyền từ nguồn đến đích. Trên thực tế, các nguồn và đích khác nhau có các thuộc tính và hành vi khác nhau có thể ảnh hưởng đến khả năng khai thác và xác định các kỹ thuật cần thiết. Ngoài ra, các tập lệnh của trang web có thể thực hiện xác thực hoặc xử lý dữ liệu khác cần được xem xét khi cố gắng khai thác lỗ hổng. Có nhiều đích liên quan đến các lỗ hổng dựa trên DOM. Vui lòng tham khảo danh sách bên dưới để biết thêm chi tiết.

Bộ xử lý này `document.write`hoạt động với `script` các phần tử, vì vậy bạn có thể sử dụng một payload đơn giản, chẳng hạn như payload bên dưới:

`document.write('... <script>alert(document.domain)</script> ...');`  

### Bài thực hành: Tấn công DOM XSS trong `document.write`sink sử dụng mã nguồn `location.search`

[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/solution/lab3.py)  

Tuy nhiên, cần lưu ý rằng trong một số trường hợp, nội dung được ghi vào `document.write` bao gồm một số ngữ cảnh xung quanh mà bạn cần phải tính đến trong quá trình khai thác. Ví dụ, bạn có thể cần phải đóng một số phần tử hiện có trước khi sử dụng mã JavaScript của mình.  

### Bài thực hành: Tấn công DOM XSS trong `document.write`sink sử dụng mã nguồn `location.search` bên trong phần tử select.

[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/solution/lab4.py)  

`innerHTML` không chấp nhận `script` các phần tử trên bất kỳ trình duyệt hiện đại nào, cũng như không `svg onload` kích hoạt các sự kiện. Điều này có nghĩa là bạn cần sử dụng các phần tử thay thế như `<div>`, `<img>` hoặc `<span>`, `<iframe>`. Các trình xử lý sự kiện như `<br> onload` và `<br> onerror` có thể được sử dụng kết hợp với các phần tử này. Ví dụ:

`element.innerHTML='... <img src=1 onerror=alert(document.domain)> ...'`  

### Bài thực hành: Tấn công DOM XSS trong `innerHTML`sink sử dụng mã nguồn `location.search`  

[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/solution/lab5.py)

## Nguồn và đích trong các phụ thuộc của bên thứ ba  
Các ứng dụng web hiện đại thường được xây dựng bằng cách sử dụng một số thư viện và framework của bên thứ ba, thường cung cấp thêm các chức năng và khả năng cho nhà phát triển. Điều quan trọng cần nhớ là một số trong số này cũng là nguồn và điểm yếu tiềm tàng của lỗ hổng DOM XSS.  

### Lỗ hổng DOM XSS trong jQuery  
Nếu đang sử dụng thư viện JavaScript như jQuery, hãy cẩn thận với các hàm có thể thay đổi các phần tử DOM trên trang. Ví dụ, hàm `attr()` của jQuery có thể thay đổi thuộc tính của các phần tử DOM. Nếu dữ liệu được đọc từ một nguồn do người dùng kiểm soát, chẳng hạn như URL, rồi được truyền vào hàm `attr()`, thì có thể thao túng giá trị được gửi để gây ra lỗ hổng XSS. Ví dụ, đây là một đoạn mã JavaScript thay đổi thuộc tính của phần tử liên kết `href` bằng cách sử dụng dữ liệu từ URL:  
```javascript
$(function() {
	$('#backLink').attr("href",(new URLSearchParams(window.location.search)).get('returnUrl'));
});
```

Bạn có thể khai thác lỗ hổng này bằng cách sửa đổi URL sao cho `location.search` nguồn chứa một URL JavaScript độc hại. Sau khi JavaScript của trang áp dụng URL độc hại này vào thuộc tính `href` của liên kết quay lại, việc nhấp vào liên kết đó sẽ thực thi URL độc hại này:

`?returnUrl=javascript:alert(document.domain)`  

### Bài thực hành: Tấn công DOM XSS trong thuộc tính `anchor` của jQuery sử dụng mã nguồn `location.search`  

[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/solution/lab6.py)  

Một lỗ hổng tiềm ẩn khác cần cảnh giác là hàm selector của jQuery, có thể được sử dụng để chèn các đối tượng độc hại vào DOM.

jQuery từng cực kỳ phổ biến, và một lỗ hổng XSS DOM kinh điển là do các trang web sử dụng bộ chọn này kết hợp với mã nguồn `location.hash` cho hoạt ảnh hoặc tự động cuộn đến một phần tử cụ thể trên trang. Hành vi này thường được thực hiện bằng cách sử dụng trình xử lý sự kiện `hashchange` dễ bị tổn thương, tương tự như sau:

```javascript
$(window).on('hashchange', function() {
	var element = $(location.hash);
	element[0].scrollIntoView();
});
```

Vì thuộc tính này `hash` có thể được người dùng điều khiển, kẻ tấn công có thể lợi dụng điều này để chèn mã XSS vào bộ chọn `$()`. Các phiên bản jQuery gần đây đã vá lỗ hổng này bằng cách ngăn chặn việc chèn HTML vào bộ chọn khi đầu vào bắt đầu bằng ký tự dấu thăng (`#`). Tuy nhiên, bạn vẫn có thể tìm thấy mã dễ bị tổn thương trong thực tế.

Để thực sự khai thác lỗ hổng kinh điển này, bạn cần tìm cách kích hoạt một sự kiện `hashchange` mà không cần sự tương tác của người dùng. Một trong những cách đơn giản nhất để làm điều này là phân phối mã khai thác của bạn thông qua một `iframe`:

```html
<iframe src="https://vulnerable-website.com#" onload="this.src+='<img src=1 onerror=alert(1)>'">
```

Trong ví dụ này, thuộc tính `src` của iframe trỏ đến trang web dễ bị tổn thương với giá trị băm rỗng. Khi trang `iframe` được tải, một mã khai thác XSS được thêm vào giá trị băm, khiến sự kiện `hashchange` được kích hoạt.  

### Bài thực hành: Tấn công XSS DOM trong bộ chọn jQuery sử dụng sự kiện hashchange  

[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/solution/lab7.py)

### Lỗ hổng DOM XSS trong AngularJS  
Nếu sử dụng một framework như AngularJS, có thể thực thi JavaScript mà không cần dấu ngoặc nhọn hoặc sự kiện. Khi một trang web sử dụng thuộc tính `ng-app` trên một phần tử HTML, nó sẽ được xử lý bởi AngularJS. Trong trường hợp này, AngularJS sẽ thực thi JavaScript bên trong dấu ngoặc nhọn kép, có thể xuất hiện trực tiếp trong HTML hoặc bên trong các thuộc tính.  

### Bài thực hành: Tấn công XSS DOM trong AngularJS bằng biểu thức có dấu ngoặc nhọn và dấu ngoặc kép (được mã hóa HTML).  

[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/solution/lab8.py)

# Lỗ hổng DOM XSS kết hợp với dữ liệu phản chiếu và lưu trữ  
Một số lỗ hổng bảo mật thuần túy dựa trên DOM chỉ tồn tại trong một trang duy nhất. Nếu một đoạn mã đọc dữ liệu từ URL và ghi nó vào một đích đến nguy hiểm, thì lỗ hổng đó hoàn toàn nằm ở phía máy khách.

Tuy nhiên, nguồn gốc của các lỗ hổng không chỉ giới hạn ở dữ liệu được trình duyệt trực tiếp hiển thị mà còn có thể bắt nguồn từ chính trang web. Ví dụ, các trang web thường phản ánh các tham số URL trong phản hồi HTML từ máy chủ. Điều này thường liên quan đến lỗ hổng XSS thông thường, nhưng nó cũng có thể dẫn đến các lỗ hổng XSS DOM phản chiếu.

Trong lỗ hổng XSS DOM phản xạ, máy chủ xử lý dữ liệu từ yêu cầu và phản hồi lại dữ liệu đó. Dữ liệu phản xạ có thể được đặt vào một chuỗi ký tự JavaScript hoặc một mục dữ liệu trong DOM, chẳng hạn như trường biểu mẫu. Sau đó, một đoạn mã trên trang sẽ xử lý dữ liệu phản xạ theo cách không an toàn, cuối cùng ghi nó vào một đích nguy hiểm.

`eval('var data = "reflected string"');`  

### Bài thực hành: Tấn công XSS vào DOM phản chiếu  

[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/solution/lab9.py)  

Các trang web cũng có thể lưu trữ dữ liệu trên máy chủ và phản ánh dữ liệu đó ở nơi khác. Trong lỗ hổng XSS DOM lưu trữ, máy chủ nhận dữ liệu từ một yêu cầu, lưu trữ dữ liệu đó, và sau đó đưa dữ liệu đó vào phản hồi sau này. Một đoạn mã trong phản hồi sau đó chứa một sink (bộ xử lý dữ liệu) sau đó xử lý dữ liệu theo cách không an toàn.

`element.innerHTML = comment.author`  

### Bài thực hành: Lỗ hổng XSS trong DOM được lưu trữ  

[Solution](https://github.com/ncKien05/PortSwigger/blob/main/Cross-site%20scripting/solution/lab10.py)  

# Những loại sink nào có thể dẫn đến lỗ hổng DOM-XSS?  
Dưới đây là một số nguyên nhân chính có thể dẫn đến lỗ hổng DOM-XSS:  

```javascript
document.write()
document.writeln()
document.domain
element.innerHTML
element.outerHTML
element.insertAdjacentHTML
element.onevent
```  

Các hàm jQuery sau đây cũng là những điểm yếu có thể dẫn đến lỗ hổng DOM-XSS:  

```javascript
add()
after()
append()
animate()
insertAfter()
insertBefore()
before()
html()
prepend()
replaceAll()
replaceWith()
wrap()
wrapInner()
wrapAll()
has()
constructor()
init()
index()
jQuery.parseHTML()
$.parseHTML()
```

# Cách phòng ngừa lỗ hổng DOM-XSS  
Ngoài các biện pháp chung được mô tả trên trang về các lỗ hổng dựa trên DOM , bạn nên tránh cho phép dữ liệu từ bất kỳ nguồn không đáng tin cậy nào được ghi động vào tài liệu HTML.  

