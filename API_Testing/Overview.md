# Kiểm thử API  
API (Giao diện lập trình ứng dụng) cho phép các hệ thống và ứng dụng phần mềm giao tiếp và chia sẻ dữ liệu. Kiểm thử API rất quan trọng vì các lỗ hổng trong API có thể làm suy yếu các khía cạnh cốt lõi về tính bảo mật, tính toàn vẹn và tính khả dụng của một trang web.  

Tất cả các trang web động đều được cấu thành từ API, vì vậy các lỗ hổng bảo mật web kinh điển như tấn công SQL injection có thể được xếp vào loại kiểm thử API. Trong chủ đề này, chúng ta sẽ hướng dẫn bạn cách kiểm thử các API không được sử dụng hoàn toàn bởi giao diện người dùng của trang web, tập trung vào các API RESTful và JSON. Chúng ta cũng sẽ hướng dẫn bạn cách kiểm thử các lỗ hổng làm ô nhiễm tham số phía máy chủ có thể ảnh hưởng đến các API nội bộ.  

Để minh họa sự chồng chéo giữa kiểm thử API và kiểm thử web nói chung, chúng tôi đã tạo ra một bảng đối chiếu giữa các chủ đề hiện có của chúng tôi và danh sách [OWASP API Security Top 10 năm 2023](https://portswigger.net/web-security/api-testing/top-10-api-vulnerabilities) .  

# Tái cấu trúc API
Để bắt đầu kiểm thử API, trước tiên bạn cần tìm hiểu càng nhiều thông tin về API càng tốt, để khám phá bề mặt tấn công của nó.  

Trước tiên, bạn cần xác định các điểm cuối API. Đây là những vị trí mà API nhận được yêu cầu về một tài nguyên cụ thể trên máy chủ của nó. Ví dụ, hãy xem xét yêu cầu `GET` sau:  
```
GET /api/books HTTP/1.1
Host: example.com
```  

Điểm cuối API cho yêu cầu này là `/api/books`. Điều này dẫn đến việc tương tác với API để truy xuất danh sách sách từ thư viện. Một điểm cuối API khác có thể là, ví dụ, `/api/books/mystery`, sẽ truy xuất danh sách sách trinh thám.  

Sau khi xác định được các điểm cuối (endpoints), bạn cần tìm hiểu cách tương tác với chúng. Điều này cho phép bạn xây dựng các yêu cầu HTTP hợp lệ để kiểm tra API. Ví dụ, bạn nên tìm hiểu thông tin về những điều sau:  

* Dữ liệu đầu vào mà API xử lý, bao gồm cả các tham số bắt buộc và tùy chọn.  
* Các loại yêu cầu mà API chấp nhận, bao gồm các phương thức HTTP và định dạng phương tiện được hỗ trợ.  
* Giới hạn tốc độ và cơ chế xác thực.  

# Tài liệu API  

Các API thường được ghi chép lại để các nhà phát triển biết cách sử dụng và tích hợp chúng.  

Tài liệu có thể ở cả dạng dễ đọc đối với con người và dạng dễ đọc đối với máy tính. Tài liệu dễ đọc đối với con người được thiết kế để các nhà phát triển hiểu cách sử dụng API. Nó có thể bao gồm các giải thích chi tiết, ví dụ và các kịch bản sử dụng. Tài liệu dễ đọc đối với máy tính được thiết kế để phần mềm xử lý nhằm tự động hóa các tác vụ như tích hợp và xác thực API. Nó được viết bằng các định dạng có cấu trúc như JSON hoặc XML.  

Tài liệu API thường được công khai, đặc biệt nếu API đó dành cho các nhà phát triển bên ngoài sử dụng. Nếu vậy, hãy luôn bắt đầu quá trình tìm hiểu bằng cách xem xét tài liệu.  

## Tìm hiểu tài liệu API  
Ngay cả khi tài liệu API không được công khai, bạn vẫn có thể truy cập được bằng cách duyệt các ứng dụng sử dụng API đó.

Để làm điều này, bạn có thể sử dụng Burp Scanner để thu thập thông tin từ API. Bạn cũng có thể duyệt các ứng dụng theo cách thủ công bằng trình duyệt của Burp. Hãy tìm kiếm các điểm cuối (endpoint) có thể tham chiếu đến tài liệu API, ví dụ:

* `/api`
* `/swagger/index.html`
* `/openapi.json`  

Nếu bạn xác định được điểm cuối (endpoint) cho một tài nguyên, hãy đảm bảo điều tra đường dẫn cơ sở. Ví dụ, nếu bạn xác định được điểm cuối của tài nguyên `/api/swagger/v1/users/123`, thì bạn nên điều tra các đường dẫn sau:

* `/api/swagger/v1`
* `/api/swagger`
* `/api`  

Bạn cũng có thể sử dụng danh sách các đường dẫn thông dụng để tìm tài liệu bằng Intruder.  

#### Bài thực hành: Khai thác điểm cuối API bằng cách sử dụng tài liệu.  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/API_Testing/Solution/lab1.py)  

## Sử dụng tài liệu có thể đọc được bằng máy tính  
Bạn có thể sử dụng nhiều công cụ tự động để phân tích bất kỳ tài liệu API nào có thể đọc được bằng máy mà bạn tìm thấy.  

Bạn có thể sử dụng Burp Scanner để thu thập thông tin và kiểm tra tài liệu OpenAPI, hoặc bất kỳ tài liệu nào khác ở định dạng JSON hoặc YAML. Bạn cũng có thể phân tích cú pháp tài liệu OpenAPI bằng ứng dụng OpenAPI Parser BApp.  

Bạn cũng có thể sử dụng một công cụ chuyên dụng để kiểm tra các điểm cuối được ghi lại, chẳng hạn như Postman hoặc SoapUI.  

# Xác định các điểm cuối API  
Bạn cũng có thể thu thập nhiều thông tin bằng cách xem xét các ứng dụng sử dụng API. Việc này thường rất đáng làm ngay cả khi bạn có tài liệu API, vì đôi khi tài liệu có thể không chính xác hoặc lỗi thời.

Bạn có thể sử dụng Burp Scanner để quét ứng dụng, sau đó tự mình điều tra các bề mặt tấn công tiềm năng bằng trình duyệt của Burp.

Trong quá trình duyệt ứng dụng, hãy tìm kiếm các mẫu gợi ý về các điểm cuối API trong cấu trúc URL, chẳng hạn như `/api/`. Cũng hãy chú ý đến các tệp JavaScript. Chúng có thể chứa các tham chiếu đến các điểm cuối API mà bạn chưa kích hoạt trực tiếp thông qua trình duyệt web. Burp Scanner tự động trích xuất một số điểm cuối trong quá trình thu thập dữ liệu, nhưng để trích xuất nhiều hơn, hãy sử dụng ứng dụng JS Link Finder BApp. Bạn cũng có thể xem xét thủ công các tệp JavaScript trong Burp.  

## Tương tác với các điểm cuối API  
Sau khi xác định được các điểm cuối API, hãy tương tác với chúng bằng Burp Repeater và Burp Intruder. Điều này cho phép bạn quan sát hành vi của API và khám phá thêm các bề mặt tấn công. Ví dụ, bạn có thể điều tra cách API phản hồi khi thay đổi phương thức HTTP và loại phương tiện.  

Khi tương tác với các điểm cuối API, hãy xem xét kỹ các thông báo lỗi và các phản hồi khác. Đôi khi, chúng bao gồm thông tin mà bạn có thể sử dụng để xây dựng một yêu cầu HTTP hợp lệ.  

### Xác định các phương thức HTTP được hỗ trợ  
Phương thức HTTP chỉ định hành động cần thực hiện trên một tài nguyên. Ví dụ:

* `GET` - Truy xuất dữ liệu từ một nguồn.  
* `PATCH` - Áp dụng các thay đổi một phần cho tài nguyên.  
* `OPTIONS` - Truy xuất thông tin về các loại phương thức yêu cầu có thể được sử dụng trên một tài nguyên.  

Một điểm cuối API có thể hỗ trợ nhiều phương thức HTTP khác nhau. Do đó, điều quan trọng là phải kiểm tra tất cả các phương thức tiềm năng khi bạn đang nghiên cứu các điểm cuối API. Điều này có thể giúp bạn xác định thêm chức năng của điểm cuối, mở ra nhiều bề mặt tấn công hơn.

Ví dụ, điểm cuối `/api/tasks` có thể hỗ trợ các phương thức sau:

* `GET /api/tasks` - Truy xuất danh sách các nhiệm vụ.  
* `POST /api/tasks` - Tạo một nhiệm vụ mới.  
* `DELETE /api/tasks/1` - Xóa một tác vụ.  

Bạn có thể sử dụng danh sách các động từ HTTP tích hợp sẵn trong Burp Intruder để tự động chuyển đổi qua một loạt các phương thức.  

### Xác định các loại nội dung được hỗ trợ  
Các điểm cuối API thường yêu cầu dữ liệu ở định dạng cụ thể. Do đó, chúng có thể hoạt động khác nhau tùy thuộc vào loại nội dung của dữ liệu được cung cấp trong yêu cầu. Thay đổi loại nội dung có thể cho phép bạn:

* Lỗi kích hoạt có thể tiết lộ thông tin hữu ích.  
* Vượt qua những điểm yếu trong hệ thống phòng thủ.  
* Hãy tận dụng những khác biệt trong logic xử lý. Ví dụ, một API có thể an toàn khi xử lý dữ liệu JSON nhưng lại dễ bị tấn công chèn mã độc khi xử lý dữ liệu XML.  

Để thay đổi loại nội dung, hãy sửa đổi `Content-Type` tiêu đề, sau đó định dạng lại phần thân yêu cầu cho phù hợp. Bạn có thể sử dụng ứng dụng BApp chuyển đổi loại nội dung để tự động chuyển đổi dữ liệu được gửi trong các yêu cầu giữa XML và JSON.  

#### Bài thực hành: Tìm kiếm và khai thác điểm cuối API chưa được sử dụng  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/API_Testing/Solution/lab2.py)    

### Sử dụng Intruder để tìm các điểm cuối ẩn.  
Sau khi xác định được một số điểm cuối API ban đầu, bạn có thể sử dụng Intruder để khám phá các điểm cuối ẩn. Ví dụ, hãy xem xét trường hợp bạn đã xác định được điểm cuối API sau đây để cập nhật thông tin người dùng:

`PUT /api/user/update`

Để xác định các điểm cuối ẩn, bạn có thể sử dụng Burp Intruder để tìm các tài nguyên khác có cấu trúc tương tự. Ví dụ, bạn có thể thêm một payload vào vị trí `/update` của đường dẫn với danh sách các hàm thông dụng khác, chẳng hạn như `delete` và `add`.

Khi tìm kiếm các điểm cuối ẩn, hãy sử dụng danh sách từ dựa trên các quy ước đặt tên API phổ biến và thuật ngữ ngành. Hãy đảm bảo bạn cũng bao gồm các thuật ngữ có liên quan đến ứng dụng, dựa trên quá trình trinh sát ban đầu của bạn.   

# Tìm kiếm các tham số ẩn  
Khi thực hiện phân tích API, bạn có thể tìm thấy các tham số không được ghi chép mà API hỗ trợ. Bạn có thể thử sử dụng chúng để thay đổi hành vi của ứng dụng. Burp bao gồm nhiều công cụ có thể giúp bạn xác định các tham số ẩn:

* Burp Intruder cho phép bạn tự động phát hiện các tham số ẩn, sử dụng danh sách từ khóa các tên tham số thông dụng để thay thế các tham số hiện có hoặc thêm các tham số mới. Hãy đảm bảo bạn cũng bao gồm các tên có liên quan đến ứng dụng, dựa trên quá trình trinh sát ban đầu của bạn.  
* Ứng dụng Param miner BApp cho phép bạn tự động đoán tối đa 65.536 tên tham số mỗi yêu cầu. Param miner tự động đoán các tên có liên quan đến ứng dụng, dựa trên thông tin lấy từ phạm vi.  
* Công cụ Khám phá Nội dung cho phép bạn khám phá nội dung không được liên kết từ nội dung hiển thị mà bạn có thể duyệt tới, bao gồm cả các tham số.  

## Các lỗ hổng phân bổ hàng loạt  
Việc gán hàng loạt (còn được gọi là tự động liên kết) có thể vô tình tạo ra các tham số ẩn. Điều này xảy ra khi các khung phần mềm tự động liên kết các tham số yêu cầu với các trường trên một đối tượng nội bộ. Do đó, việc gán hàng loạt có thể dẫn đến việc ứng dụng hỗ trợ các tham số mà nhà phát triển không hề có ý định xử lý.  
### Xác định các tham số ẩn  
Vì việc gán hàng loạt tạo ra các tham số từ các trường của đối tượng, bạn thường có thể xác định các tham số ẩn này bằng cách kiểm tra thủ công các đối tượng được API trả về.

Ví dụ, hãy xem xét một `PATCH /api/users/` yêu cầu cho phép người dùng cập nhật tên người dùng và email của họ, và yêu cầu này bao gồm JSON sau:  

```json
{
    "username": "wiener",
    "email": "wiener@example.com",
}
```
Một `GET /api/users/123` yêu cầu đồng thời trả về JSON sau:  

```json
{
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "isAdmin": "false"
}
```  

Điều này có thể cho thấy rằng các tham số ẩn `id`, `isAdmin` được liên kết với đối tượng người dùng nội bộ, cùng với các tham số tên người dùng và email đã được cập nhật.  

### Kiểm tra các lỗ hổng phân bổ khối lượng  
Để kiểm tra xem bạn có thể sửa đổi `isAdmin` giá trị của tham số được liệt kê hay không, hãy thêm nó vào `PATCH` yêu cầu:  

```json
{
    "username": "wiener",
    "email": "wiener@example.com",
    "isAdmin": false,
}
```  

Ngoài ra, hãy gửi `PATCH` yêu cầu với `isAdmin` giá trị tham số không hợp lệ:  

```json
{
    "username": "wiener",
    "email": "wiener@example.com",
    "isAdmin": "foo",
}
```  

Nếu ứng dụng hoạt động khác đi, điều này có thể cho thấy giá trị không hợp lệ ảnh hưởng đến logic truy vấn, nhưng giá trị hợp lệ thì không. Điều này có thể cho thấy người dùng có thể cập nhật tham số thành công.

Sau đó, bạn có thể gửi `PATCH` yêu cầu với `isAdmin` giá trị tham số được đặt thành `true`, để thử khai thác lỗ hổng:  

```json
{
    "username": "wiener",
    "email": "wiener@example.com",
    "isAdmin": true,
}
```  

Nếu `isAdmin` giá trị trong yêu cầu được liên kết với đối tượng người dùng mà không được xác thực và làm sạch đầy đủ, người dùng `wiener` có thể được cấp quyền quản trị một cách không chính xác. Để xác định xem đây có phải là trường hợp đó hay không, hãy duyệt ứng dụng để `wiener` xem bạn có thể truy cập chức năng quản trị hay không.  

#### Bài thực hành: Khai thác lỗ hổng phân bổ hàng loạt  
[Solution](https://github.com/ncKien05/PortSwigger/blob/main/API_Testing/Solution/lab3.py)  

# Ngăn ngừa các lỗ hổng bảo mật trong API  
Khi thiết kế API, hãy đảm bảo rằng bảo mật được xem xét ngay từ đầu. Cụ thể, hãy đảm bảo rằng bạn:

* Hãy bảo mật tài liệu của bạn nếu bạn không có ý định công khai API của mình.  
* Hãy đảm bảo tài liệu của bạn luôn được cập nhật để những người kiểm thử hợp pháp có thể nắm rõ toàn bộ các lỗ hổng bảo mật của API.  
* Áp dụng danh sách các phương thức HTTP được cho phép.  
* Xác thực xem kiểu nội dung có phù hợp với yêu cầu hoặc phản hồi hay không.  
* Hãy sử dụng các thông báo lỗi chung chung để tránh tiết lộ thông tin có thể hữu ích cho kẻ tấn công.  
* Hãy áp dụng các biện pháp bảo vệ cho tất cả các phiên bản API của bạn, chứ không chỉ phiên bản đang được sử dụng hiện tại.  

Để ngăn chặn các lỗ hổng gán giá trị hàng loạt, hãy lập danh sách cho phép các thuộc tính mà người dùng có thể cập nhật và lập danh sách chặn các thuộc tính nhạy cảm mà người dùng không nên cập nhật.



