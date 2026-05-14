# XML là gì?  
XML là viết tắt của "extensible markup language" (ngôn ngữ đánh dấu mở rộng). XML là một ngôn ngữ  được thiết kế để lưu trữ và truyền tải dữ liệu. Giống như HTML, XML sử dụng cấu trúc dạng cây gồm các thẻ và dữ liệu. Tuy nhiên, khác với HTML, XML không sử dụng các thẻ được định nghĩa trước, do đó các thẻ có thể được đặt tên mô tả dữ liệu. Trong giai đoạn đầu của lịch sử web, XML từng rất phổ biến như một định dạng truyền tải dữ liệu (chữ "X" trong "AJAX" là viết tắt của "XML"). Nhưng hiện nay, sự phổ biến của nó đã giảm sút và nhường chỗ cho định dạng JSON.  

# Các thực thể XML là gì?  
Các thực thể XML là một cách để biểu diễn một mục dữ liệu trong tài liệu XML, thay vì sử dụng chính dữ liệu đó. Nhiều thực thể được tích hợp sẵn trong đặc tả của ngôn ngữ XML. Ví dụ, các thực thể `&lt;` và `&gt;` đại diện cho các ký tự `<` và `>`. Đây là các ký tự đặc biệt được sử dụng để biểu thị các thẻ XML, và do đó, nói chung chúng phải được biểu diễn bằng các thực thể của chúng khi xuất hiện trong dữ liệu.  

# Định nghĩa loại tài liệu là gì?  
Định nghĩa kiểu tài liệu XML (DTD) chứa các khai báo có thể xác định cấu trúc của một tài liệu XML, các loại giá trị dữ liệu mà nó có thể chứa và các mục khác. DTD được khai báo trong phần tử `DOCTYPE` ở đầu tài liệu XML. DTD có thể hoàn toàn độc lập trong chính tài liệu (được gọi là "DTD nội bộ") hoặc có thể được tải từ nơi khác (được gọi là "DTD bên ngoài") hoặc có thể là sự kết hợp của cả hai. 

# Các thực thể tùy chỉnh XML là gì?  
XML cho phép định nghĩa các thực thể tùy chỉnh trong DTD. Ví dụ:

`<!DOCTYPE foo [ <!ENTITY myentity "my entity value" > ]>`  
Định nghĩa này có nghĩa là bất kỳ việc sử dụng tham chiếu thực thể `&myentity;` nào trong tài liệu XML sẽ được thay thế bằng giá trị đã định nghĩa: `my entity value`.  

# Các thực thể bên ngoài XML là gì?  
Các thực thể bên ngoài XML là một loại thực thể tùy chỉnh có định nghĩa nằm ngoài DTD nơi chúng được khai báo.  

Việc khai báo một thực thể bên ngoài sử dụng từ khóa `SYSTEM` và phải chỉ định một URL mà từ đó giá trị của thực thể sẽ được tải. Ví dụ:

`<!DOCTYPE foo [ <!ENTITY ext SYSTEM "http://normal-website.com" > ]>`  
URL có thể sử dụng giao thức `file://`, do đó các thực thể bên ngoài có thể được tải từ tệp. Ví dụ:

`<!DOCTYPE foo [ <!ENTITY ext SYSTEM "file:///path/to/file" > ]>`  
Các thực thể bên ngoài XML là phương tiện chính mà qua đó các cuộc tấn công thực thể bên ngoài XML phát sinh.  

