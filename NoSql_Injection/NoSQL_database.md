# Cơ sở dữ liệu NoSQL
Cơ sở dữ liệu NoSQL lưu trữ và truy xuất dữ liệu ở định dạng khác với các bảng quan hệ SQL truyền thống. Chúng được thiết kế để xử lý khối lượng lớn dữ liệu phi cấu trúc hoặc bán cấu trúc. Do đó, chúng thường có ít ràng buộc quan hệ và kiểm tra tính nhất quán hơn SQL, và mang lại những lợi ích đáng kể về khả năng mở rộng, tính linh hoạt và hiệu suất.

Giống như cơ sở dữ liệu SQL, người dùng tương tác với dữ liệu trong cơ sở dữ liệu NoSQL bằng cách sử dụng các truy vấn được ứng dụng gửi đến cơ sở dữ liệu. Tuy nhiên, các cơ sở dữ liệu NoSQL khác nhau sử dụng nhiều ngôn ngữ truy vấn khác nhau thay vì một tiêu chuẩn chung như SQL (Ngôn ngữ truy vấn có cấu trúc). Đó có thể là một ngôn ngữ truy vấn tùy chỉnh hoặc một ngôn ngữ phổ biến như XML hoặc JSON.

# Mô hình cơ sở dữ liệu NoSQL
Có rất nhiều loại cơ sở dữ liệu NoSQL khác nhau. Để phát hiện các lỗ hổng trong cơ sở dữ liệu NoSQL, việc hiểu rõ mô hình khung và ngôn ngữ của nó là rất hữu ích.

Một số loại cơ sở dữ liệu NoSQL phổ biến bao gồm:

* Kho lưu trữ tài liệu - Loại kho này lưu trữ dữ liệu dưới dạng các tài liệu bán cấu trúc, linh hoạt. Chúng thường sử dụng các định dạng như JSON, BSON và XML, và được truy vấn thông qua API hoặc ngôn ngữ truy vấn. Ví dụ bao gồm MongoDB và Couchbase.
* Kho lưu trữ cặp khóa-giá trị - Loại kho này lưu trữ dữ liệu ở định dạng cặp khóa-giá trị. Mỗi trường dữ liệu được liên kết với một chuỗi khóa duy nhất. Giá trị được truy xuất dựa trên khóa duy nhất đó. Ví dụ bao gồm Redis và Amazon DynamoDB.
* Các hệ thống lưu trữ dạng cột rộng - Hệ thống này tổ chức dữ liệu liên quan thành các nhóm cột linh hoạt thay vì các hàng truyền thống. Ví dụ bao gồm Apache Cassandra và Apache HBase.
* Cơ sở dữ liệu đồ thị - Loại này sử dụng các nút để lưu trữ các thực thể dữ liệu và các cạnh để lưu trữ các mối quan hệ giữa các thực thể. Ví dụ bao gồm Neo4j và Amazon Neptune.