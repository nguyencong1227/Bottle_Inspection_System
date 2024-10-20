# Hệ thống kiểm tra chai

Dự án này được tạo ra để cho phép người dùng kiểm tra chai bằng cách phân tích ảnh. Chương trình chỉ hoạt động cho các loại chai cụ thể, được chứa đầy chất lỏng có màu sắc cụ thể và đặt trên nền đặc biệt. Các bức ảnh được sử dụng trong dự án là do tôi chụp.

Các thư viện được sử dụng: OpenCV, NumPy, PyQt5

## Các giai đoạn chính của chương trình:

1. Kiểm tra nhãn hiệu của chai.
2. Kiểm tra xem chai có nhãn hay không và thêm các khung bao quanh nhãn và nắp (nếu có).
3. Kiểm tra xem có chất lỏng bên trong chai không và thêm một đường nổi bật mức chất lỏng.

Mỗi giai đoạn chính của chương trình bao gồm các bước nhỏ hơn. Các bước cho từng giai đoạn được liệt kê dưới đây.

### Kiểm tra nhãn hiệu của chai:

1. Nhận hình ảnh của hình dạng chai.
2. Cắt và điều chỉnh hình ảnh để đặt chiều rộng của chai ở giá trị cố định.
3. So sánh với các hình dạng mẫu.

### Kiểm tra xem có nhãn trên chai hay không và thêm khung bao quanh nhãn và nắp (nếu có):

1. Tìm các điểm chính trên ảnh chai và các hình ảnh với nhãn mẫu.
2. So sánh các điểm chính tìm được và xác định xem có nhãn phù hợp (hoặc phù hợp nhất) hay không.
3. Kiểm tra vị trí của nhãn và nắp trên ảnh.
4. Thêm khung bao vào ảnh.

### Kiểm tra xem có chất lỏng bên trong chai không và thêm một đường nổi bật mức chất lỏng:

1. Chuyển ảnh từ chế độ BGR sang HSV và thêm các mặt nạ.
2. Kiểm tra xem có chất lỏng hay không bằng cách kiểm tra số lượng điểm ảnh đại diện cho một trong hai màu của chất lỏng và so sánh số lượng này với số lượng điểm ảnh đại diện cho hình dạng chai.
3. Kiểm tra mức chất lỏng bằng cách sử dụng biểu đồ ngang và một hình ảnh với các điểm ảnh đại diện cho màu chất lỏng được tô trắng trên nền đen.
4. Thêm một đường màu đỏ để làm nổi bật mức chất lỏng trên ảnh.
