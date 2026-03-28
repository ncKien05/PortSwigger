# Path traversal
Trong phần này, chúng tôi sẽ giải thích:

* Thuật toán path traversal là gì?  
* Cách thực hiện các cuộc tấn công path traversal và vượt qua các chướng ngại vật thường gặp.  
* Cách ngăn chặn các lỗ hổng path traversal. 

Trong một số trường hợp, kẻ tấn công có thể ghi vào các tệp tùy ý trên máy chủ, cho phép chúng sửa đổi dữ liệu hoặc hành vi của ứng dụng, và cuối cùng giành quyền kiểm soát hoàn toàn máy chủ.  

# Đọc các tập tin tùy ý thông qua duyệt đường dẫn

Hãy tưởng tượng một ứng dụng mua sắm hiển thị hình ảnh các mặt hàng đang bán. Ứng dụng này có thể tải hình ảnh bằng mã HTML sau:  
`<img src="/loadImage?filename=218.png">`  

URL này `loadImage` nhận một `filename` tham số và trả về nội dung của tệp được chỉ định. Các tệp hình ảnh được lưu trữ trên đĩa tại vị trí `/var/www/images/`. Để trả về một hình ảnh, ứng dụng sẽ thêm tên tệp được yêu cầu vào thư mục gốc này và sử dụng API hệ thống tệp để đọc nội dung của tệp. Nói cách khác, ứng dụng đọc từ đường dẫn tệp sau:  
`/var/www/images/218.png`  

Ứng dụng này không có bất kỳ biện pháp phòng vệ nào chống lại các cuộc tấn công vượt quyền truy cập thư mục. Do đó, kẻ tấn công có thể yêu cầu URL sau để truy xuất `/etc/passwd` tệp từ hệ thống tệp của máy chủ:  
`https://insecure-website.com/loadImage?filename=../../../../etc/passwd`  

Điều này khiến ứng dụng đọc dữ liệu từ đường dẫn tệp sau:  
`/var/www/images/../../../etc/passwd`  

Chuỗi ký tự này `../` hợp lệ trong đường dẫn tệp và có nghĩa là di chuyển lên một cấp trong cấu trúc thư mục. Ba chuỗi `../` ký tự liên tiếp di chuyển từ `/var/www/images/` thư mục gốc của hệ thống tệp, do đó tệp thực sự được đọc là:  
`/etc/passwd`  

Trên các hệ điều hành dựa trên Unix, đây là một tập tin chuẩn chứa thông tin chi tiết về người dùng đã đăng ký trên máy chủ, nhưng kẻ tấn công có thể lấy được các tập tin tùy ý khác bằng kỹ thuật tương tự.

Trên Windows, cả hai lệnh `../`và `..\`đều là các chuỗi tấn công duyệt thư mục hợp lệ. Sau đây là một ví dụ về cuộc tấn công tương đương nhằm vào máy chủ chạy hệ điều hành Windows:  
`https://insecure-website.com/loadImage?filename=../../../../windows/win.ini`  

## Bài thực hành: Tấn công vượt quyền truy cập tệp, trường hợp đơn giản  
[SOLUTION](https://github.com/ncKien05/PortSwigger/blob/main/Path%20Traversal/Solution/lab1.py)  

# Những trở ngại thường gặp khi khai thác lỗ hổng vượt quyền truy cập đường dẫn  

Nhiều ứng dụng đặt dữ liệu nhập từ người dùng vào đường dẫn tệp tin và triển khai các biện pháp phòng chống tấn công duyệt thư mục. Tuy nhiên, các biện pháp này thường có thể bị vượt qua.  

Nếu một ứng dụng loại bỏ hoặc chặn các chuỗi tấn công duyệt thư mục khỏi tên tệp do người dùng cung cấp, thì có thể vượt qua biện pháp phòng vệ đó bằng nhiều kỹ thuật khác nhau.  

Bạn có thể sử dụng đường dẫn tuyệt đối từ thư mục gốc của hệ thống tệp, chẳng hạn như `filename=/etc/passwd`, để tham chiếu trực tiếp đến một tệp mà không cần sử dụng bất kỳ chuỗi duyệt nào.  

## Bài thực hành: Tấn công vượt quyền truy cập tệp, các chuỗi tấn công bị chặn bằng cách bỏ qua đường dẫn tuyệt đối.  
[SOLUTION](https://github.com/ncKien05/PortSwigger/blob/main/Path%20Traversal/Solution/lab2.py)  

Bạn có thể sử dụng các chuỗi duyệt lồng nhau, chẳng hạn như `....//` hoặc `....\/`. Chúng sẽ trở lại thành các chuỗi duyệt đơn giản khi chuỗi bên trong bị loại bỏ.  

## Bài thực hành: Duyệt đường dẫn tập tin, chuỗi duyệt được loại bỏ không đệ quy  
[SOLUTION](https://github.com/ncKien05/PortSwigger/blob/main/Path%20Traversal/Solution/lab3.py)  

Trong một số ngữ cảnh, chẳng hạn như trong đường dẫn URL hoặc tham `filename` số của `multipart/form-data` yêu cầu, máy chủ web có thể loại bỏ bất kỳ chuỗi duyệt thư mục nào trước khi chuyển dữ liệu đầu vào của bạn đến ứng dụng. Đôi khi bạn có thể bỏ qua kiểu làm sạch này bằng cách mã hóa URL, hoặc thậm chí mã hóa URL kép, các `../` ký tự. Điều này dẫn đến kết quả tương ứng là `%2e%2e%2f` và `%252e%252e%252f`. Nhiều mã hóa không chuẩn khác, chẳng hạn như `..%c0%af` hoặc `..%ef%bc%8f`, cũng có thể hoạt động.

Đối với người dùng Burp Suite Professional, Burp Intruder cung cấp danh sách payload được định sẵn **Fuzzing - path traversal**. Danh sách này chứa một số chuỗi tấn công duyệt đường dẫn được mã hóa mà bạn có thể thử.  

## Bài thực hành: Tấn công duyệt đường dẫn tệp, chuỗi duyệt được loại bỏ bằng cách giải mã URL thừa.  
[SOLUTION](https://github.com/ncKien05/PortSwigger/blob/main/Path%20Traversal/Solution/lab4.py)  

Một ứng dụng có thể yêu cầu tên tệp do người dùng cung cấp phải bắt đầu bằng thư mục gốc dự kiến, chẳng hạn như `/var/www/images`. Trong trường hợp này, có thể bao gồm thư mục gốc cần thiết theo sau là các chuỗi duyệt phù hợp. Ví dụ: `filename=/var/www/images/../../../etc/passwd`.  

## Bài thực hành: Duyệt đường dẫn tệp, xác thực điểm bắt đầu của đường dẫn.  
[SOLUTION](https://github.com/ncKien05/PortSwigger/blob/main/Path%20Traversal/Solution/lab5.py)  

Một ứng dụng có thể yêu cầu tên tệp do người dùng cung cấp phải kết thúc bằng phần mở rộng tệp dự kiến, chẳng hạn như `.png`. Trong trường hợp này, có thể sử dụng một byte null để kết thúc đường dẫn tệp trước phần mở rộng bắt buộc. Ví dụ: `filename=../../../etc/passwd%00.png`.       

## Bài thực hành: Tấn công duyệt đường dẫn tệp, xác thực phần mở rộng tệp bằng cách bỏ qua ký tự null.  
[SOLUTION](https://github.com/ncKien05/PortSwigger/blob/main/Path%20Traversal/Solution/lab6.py)  

# Cách ngăn chặn tấn công duyệt thư mục  

Cách hiệu quả nhất để ngăn chặn các lỗ hổng tấn công vượt quyền truy cập thư mục là tránh hoàn toàn việc truyền dữ liệu do người dùng cung cấp cho các API hệ thống tập tin. Nhiều chức năng ứng dụng thực hiện việc này có thể được viết lại để cung cấp cùng một hành vi theo cách an toàn hơn.

Nếu bạn không thể tránh việc truyền dữ liệu do người dùng cung cấp cho các API hệ thống tập tin, chúng tôi khuyên bạn nên sử dụng hai lớp bảo vệ để ngăn chặn các cuộc tấn công:

* Xác thực dữ liệu người dùng nhập vào trước khi xử lý. Tốt nhất là nên so sánh dữ liệu người dùng nhập vào với danh sách các giá trị được cho phép. Nếu điều đó không thể thực hiện được, hãy kiểm tra xem dữ liệu nhập vào chỉ chứa nội dung được cho phép, chẳng hạn như chỉ chứa các ký tự chữ và số.  
* Sau khi xác thực dữ liệu đầu vào, hãy thêm dữ liệu đó vào thư mục gốc và sử dụng API hệ thống tệp của nền tảng để chuẩn hóa đường dẫn. Kiểm tra xem đường dẫn đã chuẩn hóa có bắt đầu từ thư mục gốc như mong đợi hay không.  

Dưới đây là một ví dụ về đoạn mã Java đơn giản để xác thực đường dẫn chính tắc của một tệp dựa trên dữ liệu người dùng nhập vào:  

```
File file = new File(BASE_DIRECTORY, userInput);
if (file.getCanonicalPath().startsWith(BASE_DIRECTORY)) {
    // process file
}
```  



