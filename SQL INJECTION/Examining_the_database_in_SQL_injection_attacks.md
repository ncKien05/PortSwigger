# Kiểm tra cơ sở dữ liệu trong các cuộc tấn công SQL injection
Để khai thác các lỗ hổng tấn công SQL injection, thường cần phải tìm kiếm thông tin về cơ sở dữ liệu. Điều này bao gồm:  
* Loại và phiên bản phần mềm cơ sở dữ liệu.
* Các bảng và cột mà cơ sở dữ liệu chứa.  

# Truy vấn loại và phiên bản cơ sở dữ liệu  
Bạn có thể xác định cả loại và phiên bản cơ sở dữ liệu bằng cách chèn các truy vấn dành riêng cho nhà cung cấp để xem liệu có truy vấn nào hoạt động hay không.  

Dưới đây là một số truy vấn để xác định phiên bản cơ sở dữ liệu cho một số loại cơ sở dữ liệu phổ biến:  
| Database type | Query |
| :--- | :--- |
| Microsoft, MySQL | `SELECT @@version`
| Oracle | `SELECT * FROM v$version`  
| PostgreSQL | `SELECT version()`

## Bài thực hành: Tấn công SQL injection, truy vấn loại và phiên bản cơ sở dữ liệu trên Oracle.
[Solution](./solution/lab4.py)
## Bài thực hành: Tấn công SQL injection, truy vấn loại và phiên bản cơ sở dữ liệu trên MySQL và Microsoft.
[Solution](./solution/lab5.py)  
# Liệt kê nội dung của cơ sở dữ liệu
Hầu hết các loại cơ sở dữ liệu (ngoại trừ Oracle) đều có một tập hợp các khung nhìn được gọi là lược đồ thông tin. Lược đồ này cung cấp thông tin về cơ sở dữ liệu.  
Ví dụ, bạn có thể truy vấn `information_schema.tables`để liệt kê các bảng trong cơ sở dữ liệu:  

`SELECT * FROM information_schema.tables`  

Bạn có thể truy vấn `information_schema.columns` để liệt kê các cột trong từng bảng riêng lẻ:  
## Bài thực hành: Tấn công SQL injection, liệt kê nội dung cơ sở dữ liệu trên các cơ sở dữ liệu không phải Oracle.  
[Solution](./solution/lab6.py)  

# Liệt kê nội dung của cơ sở dữ liệu Oracle  
Trên Oracle, bạn có thể tìm thấy thông tin tương tự như sau:  
Bạn có thể liệt kê các bảng bằng cách truy vấn all_tables:  
`SELECT * FROM all_tables`  
Bạn có thể liệt kê các cột bằng cách truy vấn all_tab_columns:  
`SELECT * FROM all_tab_columns WHERE table_name = 'USERS'`  
## Bài thực hành: Tấn công SQL injection, liệt kê nội dung cơ sở dữ liệu trên Oracle.  
[Solution](./solution/lab7.py) 


