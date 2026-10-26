# Personal Expense Tracker

Ứng dụng console nhỏ để ghi lại các khoản chi tiêu cá nhân. Đây là capstone cho Tuần 15 của Python Journey, dùng thư viện chuẩn của Python khi chạy ứng dụng; `pytest` chỉ cần cho kiểm thử.

## Chức năng

- Thêm giao dịch với mô tả, danh mục và số tiền.
- Xem danh sách giao dịch.
- Tính tổng chi tiêu.
- Lọc giao dịch theo danh mục, không phân biệt chữ hoa/chữ thường.
- Lưu và đọc dữ liệu từ file JSON.
- Kiểm tra dữ liệu đầu vào và báo lỗi khi dữ liệu lưu không hợp lệ.

Ứng dụng hiện quản lý **chi tiêu**; chưa tách riêng thu nhập, ngân sách, giao dịch định kỳ, biểu đồ hay nhiều loại tiền tệ.

## Yêu cầu

- Python 3.12 trở lên.
- `pytest` để chạy bộ test.

## Chạy ứng dụng

Mở terminal tại thư mục `projects/expense-tracker`:

```bash
python main.py
```

Chọn một mục trong menu:

| Lựa chọn | Chức năng |
|---|---|
| `1` | Thêm giao dịch |
| `2` | Xem các giao dịch |
| `3` | Xem tổng chi tiêu |
| `4` | Lọc theo danh mục |
| `5` | Lưu dữ liệu |
| `0` | Thoát |

**Lưu ý:** cần chọn mục `5` để lưu các thay đổi. Ứng dụng không tự động lưu khi thoát.

### Ví dụ sử dụng

Ví dụ thêm một khoản chi:

```text
Chon: 1
Mo ta: Lunch
Danh muc: Food
So tien: 50
Da them giao dich.
```

Sau đó chọn `3` để xem tổng:

```text
Chon: 3
Tong chi tieu: 50.00
```

Thông báo trong terminal hiện dùng tiếng Việt không dấu để tương thích đơn giản với môi trường terminal khác nhau.

## Dữ liệu và xác thực

Khi lưu, ứng dụng ghi danh sách giao dịch vào:

```text
data/transactions.json
```

Thư mục `data` được tạo khi lưu nếu chưa tồn tại. Nếu file chưa có, ứng dụng bắt đầu với danh sách trống. Khi đọc file có JSON sai định dạng hoặc giao dịch thiếu trường bắt buộc, chương trình báo lỗi đọc dữ liệu và tiếp tục với danh sách trống trong phiên hiện tại; dữ liệu lỗi không được tự động sửa hoặc ghi đè.

Mỗi giao dịch có ba trường:

- `description`: mô tả không được để trống;
- `category`: danh mục không được để trống;
- `amount`: số hữu hạn lớn hơn 0.

Khoảng trắng đầu/cuối của mô tả và danh mục được loại bỏ. Bộ lọc danh mục không phân biệt chữ hoa/chữ thường.

## Chạy kiểm thử

Từ thư mục `projects/expense-tracker`, cài pytest nếu máy chưa có:

```bash
python -m pip install pytest
```

Sau đó chạy:

```bash
python -m pytest -q
```

Bộ test bao gồm kiểm tra dữ liệu hợp lệ và không hợp lệ, tổng chi tiêu, lọc danh mục, danh sách trống, lưu/đọc JSON, file chưa tồn tại, JSON sai định dạng và trường giao dịch bị thiếu.

> Chỉ xem test là đã đạt sau khi bạn tự chạy lệnh trên và kiểm tra kết quả trên máy của mình.

## Cấu trúc code

```text
expense-tracker/
├── main.py            # Menu và nhập/xuất terminal
├── src/
│   ├── __init__.py
│   ├── core.py        # Quy tắc nghiệp vụ và xác thực giao dịch
│   └── storage.py     # Đọc/ghi JSON
├── tests/
│   └── test_core.py   # Kiểm thử tự động
├── data/              # Được tạo khi lưu dữ liệu
├── README.md
└── AI_USAGE.md        # Ghi nhận việc sử dụng AI
```

Quy tắc nghiệp vụ được tách khỏi phần nhập liệu để có thể kiểm thử mà không cần tương tác với menu. `storage.py` kiểm tra dữ liệu khi đọc JSON thay vì mặc định tin mọi nội dung trong file.

## Giới hạn và lưu ý

Đây là ứng dụng học tập chạy cục bộ cho một người dùng. File JSON không được mã hóa; không lưu dữ liệu nhạy cảm vào đó. Ứng dụng không đồng bộ giữa thiết bị và chưa có cơ chế sao lưu tự động.

Xem [AI_USAGE.md](AI_USAGE.md) để ghi rõ phần AI hỗ trợ, phần bạn tự chỉnh sửa, và những gì bạn đã thực sự kiểm chứng.
