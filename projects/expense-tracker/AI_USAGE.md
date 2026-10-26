# AI Usage

## Tôi đã dùng AI cho việc gì?

- Hỗ trợ phác thảo cấu trúc module và các trường hợp kiểm thử cho capstone.
- Review các trường hợp lỗi khi đọc JSON và kiểm tra dữ liệu giao dịch.

## Tôi đã tự viết hoặc thay đổi phần nào?

- Hãy đọc lại từng module và ghi rõ các phần bạn trực tiếp viết hoặc chỉnh sửa trước khi nộp.
- Nếu bạn thay đổi thiết kế so với bản hiện tại, cập nhật mục này để phản ánh đúng quá trình làm việc.

## Tôi đã kiểm chứng câu trả lời của AI như thế nào?

- Chạy `python -m pytest -q` trong thư mục dự án sau khi tự kiểm tra code.
- Thử số tiền bằng 0 hoặc âm, mô tả rỗng, file JSON không hợp lệ và file dữ liệu chưa tồn tại.
- Đọc lại logic trong `src/core.py` và `src/storage.py` để chắc chắn hiểu cách xác thực và lưu dữ liệu.

## Một điều tôi hiểu rõ hơn

Điền bằng lời của bạn sau khi chạy và giải thích lại chương trình. Ví dụ: vì sao tách quy tắc nghiệp vụ khỏi phần nhập liệu giúp viết test dễ hơn.
