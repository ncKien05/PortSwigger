# Ô nhiễm tham số phía máy chủ  
Một số hệ thống chứa các API nội bộ không thể truy cập trực tiếp từ internet. Hiện tượng ô nhiễm tham số phía máy chủ xảy ra khi một trang web nhúng dữ liệu đầu vào của người dùng vào yêu cầu phía máy chủ gửi đến API nội bộ mà không mã hóa đầy đủ. Điều này có nghĩa là kẻ tấn công có thể thao túng hoặc chèn các tham số, từ đó cho phép chúng thực hiện các hành động như:

* Ghi đè các tham số hiện có.  
* Thay đổi hành vi của ứng dụng.  
* Truy cập dữ liệu trái phép.  

Bạn có thể kiểm tra bất kỳ dữ liệu đầu vào nào của người dùng để phát hiện bất kỳ loại tham số nào bị lỗi. Ví dụ, các tham số truy vấn, trường biểu mẫu, tiêu đề và tham số đường dẫn URL đều có thể dễ bị tấn công.  

# Kiểm tra hiện tượng nhiễu tham số phía máy chủ trong chuỗi truy vấn  
Để kiểm tra hiện tượng nhiễu tham số phía máy chủ trong chuỗi truy vấn, hãy đặt các ký tự cú pháp truy vấn như `#`, `&`, và `=`vào đầu vào của bạn và quan sát cách ứng dụng phản hồi.

Hãy xem xét một ứng dụng dễ bị tấn công cho phép bạn tìm kiếm người dùng khác dựa trên tên người dùng của họ. Khi bạn tìm kiếm một người dùng, trình duyệt của bạn sẽ thực hiện yêu cầu sau:

`GET /userSearch?name=peter&back=/home`  

Để truy xuất thông tin người dùng, máy chủ sẽ truy vấn một API nội bộ với yêu cầu sau:

`GET /users/search?name=peter&publicProfile=true`  

## Cắt ngắn chuỗi truy vấn  

Bạn có thể sử dụng ký tự được mã hóa URL `#` để cố gắng cắt bớt yêu cầu phía máy chủ. Để giúp bạn hiểu phản hồi, bạn cũng có thể thêm một chuỗi sau `#` ký tự đó.

Ví dụ, bạn có thể sửa đổi chuỗi truy vấn thành như sau:

`GET /userSearch?name=peter%23foo&back=/home`  

Giao diện người dùng sẽ cố gắng truy cập URL sau:

`GET /users/search?name=peter#foo&publicProfile=true`  

Hãy xem xét phản hồi để tìm manh mối về việc truy vấn có bị cắt ngắn hay không. Ví dụ, nếu phản hồi trả về người dùng `peter`, thì truy vấn phía máy chủ có thể đã bị cắt ngắn. Nếu `Invalid name` trả về thông báo lỗi, ứng dụng có thể đã coi `foo` là một phần của tên người dùng. Điều này cho thấy rằng yêu cầu phía máy chủ có thể không bị cắt ngắn.

Nếu bạn có thể rút gọn yêu cầu phía máy chủ, điều này sẽ loại bỏ yêu cầu trường đó `publicProfile` phải được đặt thành `true`. Bạn có thể tận dụng điều này để trả về các hồ sơ người dùng không công khai.  

## Chèn các tham số không hợp lệ  
Bạn có thể sử dụng ký tự được mã hóa URL `&` để thử thêm tham số thứ hai vào yêu cầu phía máy chủ.

Ví dụ, bạn có thể sửa đổi chuỗi truy vấn thành như sau:

`GET /userSearch?name=peter%26foo=xyz&back=/home`  

Điều này dẫn đến yêu cầu phía máy chủ sau đây gửi đến API nội bộ:

`GET /users/search?name=peter&foo=xyz&publicProfile=true`  

Hãy xem xét phản hồi để tìm manh mối về cách tham số bổ sung được phân tích cú pháp. Ví dụ, nếu phản hồi không thay đổi, điều này có thể cho thấy tham số đã được chèn thành công nhưng bị ứng dụng bỏ qua.

Để có được bức tranh toàn diện hơn, bạn cần tiến hành thêm các xét nghiệm.  

## Chèn các tham số hợp lệ  

Nếu bạn có thể sửa đổi chuỗi truy vấn, bạn có thể thử thêm tham số hợp lệ thứ hai vào yêu cầu phía máy chủ.  
Ví dụ, nếu bạn đã xác định được `email` tham số, bạn có thể thêm nó vào chuỗi truy vấn như sau:

`GET /userSearch?name=peter%26email=foo&back=/home`  

Điều này dẫn đến yêu cầu phía máy chủ sau đây gửi đến API nội bộ:

`GET /users/search?name=peter&email=foo&publicProfile=true`  

Hãy xem lại phản hồi để tìm manh mối về cách tham số bổ sung được phân tích cú pháp.  

## Ghi đè các tham số hiện có  
Để xác nhận xem ứng dụng có dễ bị tấn công bằng cách thay đổi tham số phía máy chủ hay không, bạn có thể thử ghi đè tham số gốc. Hãy thực hiện điều này bằng cách chèn thêm một tham số thứ hai có cùng tên.

Ví dụ, bạn có thể sửa đổi chuỗi truy vấn thành như sau:

`GET /userSearch?name=peter%26name=carlos&back=/home`  

Điều này dẫn đến yêu cầu phía máy chủ sau đây gửi đến API nội bộ:

`GET /users/search?name=peter&name=carlos&publicProfile=true`  

API nội bộ diễn giải hai `name` tham số. Tác động của điều này phụ thuộc vào cách ứng dụng xử lý tham số thứ hai. Điều này khác nhau giữa các công nghệ web khác nhau. Ví dụ:

* PHP chỉ phân tích tham số cuối cùng. Điều này sẽ dẫn đến việc người dùng tìm kiếm `carlos`.  
* ASP.NET kết hợp cả hai tham số. Điều này sẽ dẫn đến việc người dùng tìm kiếm `peter,carlos`, và có thể dẫn đến `Invalid username` thông báo lỗi.  
* Node.js/Express chỉ phân tích tham số đầu tiên. Điều này sẽ dẫn đến việc người dùng tìm kiếm `peter`, nhưng kết quả vẫn không thay đổi.  

Nếu bạn có thể ghi đè tham số gốc, bạn có thể thực hiện một cuộc tấn công khai thác. Ví dụ, bạn có thể thêm `name=administrator` vào yêu cầu. Điều này có thể cho phép bạn đăng nhập với tư cách người dùng quản trị.  

#### Bài thực hành: Khai thác lỗi làm sai lệch tham số phía máy chủ trong chuỗi truy vấn  

[Solution](https://github.com/ncKien05/PortSwigger/blob/main/API_Testing/Solution/lab4.py)  

# Kiểm tra lỗi ô nhiễm tham số phía máy chủ trong các đường dẫn REST  
API RESTful có thể đặt tên và giá trị tham số trong đường dẫn URL, thay vì chuỗi truy vấn. Ví dụ, hãy xem xét đường dẫn sau:

`/api/users/123`  

Đường dẫn URL có thể được phân tích như sau:

* `/api` là điểm cuối API gốc.  
* `/users` trong trường hợp này, nó đại diện cho một nguồn lực `users`.  
* `/123` biểu thị một tham số, ở đây là mã định danh cho người dùng cụ thể.  
Hãy xem xét một ứng dụng cho phép bạn chỉnh sửa hồ sơ người dùng dựa trên tên người dùng của họ. Các yêu cầu được gửi đến điểm cuối sau:

`GET /edit_profile.php?name=peter`  

Điều này dẫn đến yêu cầu phía máy chủ như sau:

`GET /api/private/users/peter`  

Kẻ tấn công có thể thao túng các tham số đường dẫn URL phía máy chủ để khai thác API. Để kiểm tra lỗ hổng này, hãy thêm các chuỗi tấn công duyệt thư mục để sửa đổi các tham số và quan sát cách ứng dụng phản hồi.

Bạn có thể gửi URL đã được mã hóa `peter/../admin` làm giá trị của `name` tham số:

`GET /edit_profile.php?name=peter%2f..%2fadmin`  

Điều này có thể dẫn đến yêu cầu phía máy chủ sau:

`GET /api/private/users/peter/../admin`  
Nếu máy khách phía máy chủ hoặc API phụ trợ chuẩn hóa đường dẫn này, nó có thể được giải quyết thành `/api/private/users/admin` .  

#### Bài thực hành: Khai thác lỗi làm sai lệch tham số phía máy chủ trong URL REST  

[Solution](https://github.com/ncKien05/PortSwigger/blob/main/API_Testing/Solution/lab5.py)  

# Kiểm tra lỗi nhiễu tham số phía máy chủ trong các định dạng dữ liệu có cấu trúc  
Kẻ tấn công có thể thao túng các tham số để khai thác các lỗ hổng trong quá trình xử lý các định dạng dữ liệu có cấu trúc khác của máy chủ, chẳng hạn như JSON hoặc XML. Để kiểm tra điều này, hãy chèn dữ liệu có cấu trúc không mong muốn vào dữ liệu đầu vào của người dùng và xem phản hồi của máy chủ.

Hãy xem xét một ứng dụng cho phép người dùng chỉnh sửa hồ sơ của họ, sau đó áp dụng các thay đổi bằng cách gửi yêu cầu đến API phía máy chủ. Khi bạn chỉnh sửa tên của mình, trình duyệt sẽ thực hiện yêu cầu sau:
```
POST /myaccount
name=peter
```
Điều này dẫn đến yêu cầu phía máy chủ như sau:
```
PATCH /users/7312/update
{"name":"peter"}
```
Bạn có thể thử thêm `access_level` tham số vào yêu cầu như sau:
```
POST /myaccount
name=peter","access_level":"administrator
```
Nếu dữ liệu do người dùng nhập được thêm vào dữ liệu JSON phía máy chủ mà không được xác thực hoặc làm sạch đầy đủ, điều này sẽ dẫn đến yêu cầu phía máy chủ như sau:
```
PATCH /users/7312/update
{name="peter","access_level":"administrator"}
```
Điều này có thể dẫn đến việc người dùng `peter` được cấp quyền quản trị.  

Hãy xem xét một ví dụ tương tự, nhưng trong đó dữ liệu người dùng nhập vào phía máy khách là dữ liệu JSON. Khi bạn chỉnh sửa tên của mình, trình duyệt sẽ thực hiện yêu cầu sau:
```
POST /myaccount
{"name": "peter"}
```
Điều này dẫn đến yêu cầu phía máy chủ như sau:
```
PATCH /users/7312/update
{"name":"peter"}
```
Bạn có thể thử thêm `access_level` tham số vào yêu cầu như sau:
```
POST /myaccount
{"name": "peter\",\"access_level\":\"administrator  "}
```
Nếu dữ liệu người dùng nhập vào được giải mã, sau đó được thêm vào dữ liệu JSON phía máy chủ mà không được mã hóa đầy đủ, điều này sẽ dẫn đến yêu cầu phía máy chủ như sau:
```
PATCH /users/7312/update
{"name":"peter","access_level":"administrator"}
```
Điều này có thể dẫn đến việc người dùng `peter` được cấp quyền quản trị.

Lỗi tấn công chèn định dạng cấu trúc cũng có thể xảy ra trong phản hồi. Ví dụ, điều này có thể xảy ra nếu dữ liệu người dùng nhập được lưu trữ an toàn trong cơ sở dữ liệu, sau đó được nhúng vào phản hồi JSON từ API phía máy chủ mà không được mã hóa đầy đủ. Thông thường, bạn có thể phát hiện và khai thác lỗi tấn công chèn định dạng cấu trúc trong phản hồi theo cùng một cách như trong yêu cầu.  

# Kiểm thử bằng các công cụ tự động  
Burp bao gồm các công cụ tự động có thể giúp bạn phát hiện các lỗ hổng làm ô nhiễm tham số phía máy chủ.

Burp Scanner tự động phát hiện các biến đổi đầu vào đáng ngờ khi thực hiện kiểm tra. Điều này xảy ra khi một ứng dụng nhận đầu vào từ người dùng, biến đổi nó theo một cách nào đó, sau đó thực hiện xử lý tiếp theo trên kết quả. Hành vi này không nhất thiết cấu thành lỗ hổng bảo mật, vì vậy bạn cần thực hiện kiểm tra thêm bằng các kỹ thuật thủ công được nêu ở trên. Để biết thêm thông tin, hãy xem định nghĩa vấn đề Biến đổi đầu vào đáng ngờ .

Bạn cũng có thể sử dụng ứng dụng Backslash Powered Scanner BApp để xác định các lỗ hổng tấn công chèn mã phía máy chủ. Trình quét phân loại các đầu vào là nhàm chán, thú vị hoặc dễ bị tổn thương. Bạn cần điều tra các đầu vào thú vị bằng các kỹ thuật thủ công được nêu ở trên. Để biết thêm thông tin, hãy xem tài liệu chuyên đề Backslash Powered Scanning: hunting unknown vulnerability classes .

# Ngăn chặn sự xâm phạm tham số phía máy chủ  
Để ngăn chặn tình trạng ô nhiễm tham số phía máy chủ, hãy sử dụng danh sách cho phép để xác định các ký tự không cần mã hóa, và đảm bảo tất cả các dữ liệu đầu vào khác của người dùng đều được mã hóa trước khi được đưa vào yêu cầu phía máy chủ. Bạn cũng nên đảm bảo rằng tất cả dữ liệu đầu vào tuân thủ định dạng và cấu trúc được mong đợi.  