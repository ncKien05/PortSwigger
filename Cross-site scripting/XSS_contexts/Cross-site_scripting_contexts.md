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