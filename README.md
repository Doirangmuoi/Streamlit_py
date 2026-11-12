# Dashboard doanh số E-Commerce

Ứng dụng Streamlit sử dụng schema của bài tập 10: `Orders`, `OrderDetails`, `Products`, `Customers` và `Categories`.

## Chạy ứng dụng

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Nhập máy chủ, cổng, tài khoản, mật khẩu và tên CSDL tại thanh bên, sau đó chọn **Kết nối / Làm mới**. Tài khoản MySQL cần quyền SELECT trên năm bảng. Dữ liệu được tải lại khi nhấn nút; thông tin kết nối không được lưu trong mã nguồn.

Mặc định chỉ chọn đơn `Completed`. Doanh thu là tổng `quantity * unit_price` của các dòng khớp bộ lọc; khi chọn `Pending` hoặc `Cancelled`, giá trị của các đơn đó cũng được tính. Bộ lọc danh mục chỉ tính những dòng sản phẩm thuộc danh mục đã chọn. Số đơn là số mã đơn khác nhau trong các dòng đó, và AOV là doanh thu chia cho số đơn. Đơn không có chi tiết không xuất hiện. Top 5 xếp theo số lượng sản phẩm. Đơn vị tiền tệ theo dữ liệu nguồn.
