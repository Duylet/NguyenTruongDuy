# Tuần 13 — Modules, Packages, CLI và HTTP

Tuần này chuyển từ các đoạn code đơn lẻ sang chương trình có cấu trúc: chia code thành module/package, nhận tham số từ terminal và đọc HTTP response qua fixture offline. Mục tiêu là hiểu cách các phần phối hợp với nhau, không phải xây một API server hoàn chỉnh.

## Mục tiêu học tập

Sau tuần này, bạn có thể:

- import module của Python và module tự viết;
- nhận biết vai trò của package và file `__init__.py`;
- dùng `if __name__ == "__main__":` để kiểm soát điểm bắt đầu chương trình;
- hiểu mục đích của virtual environment, `python -m pip` và `pyproject.toml`;
- tạo CLI đơn giản bằng `argparse`;
- nhận biết HTTP GET, status code và JSON response;
- xử lý status không thành công và JSON không hợp lệ;
- giữ logic xử lý của bot tách biệt với phần giao tiếp/adaptor.

## Cấu trúc chính

- `bot_course/core.py`: logic chọn hành động, không phụ thuộc mạng.
- `bot_course/adapter.py`: chuyển state sang kết quả theo contract của khóa học.
- `bot_course/http_foundation.py`: ví dụ xây GET request và đọc response.
- `cli.py`: nhận tham số `--position` và `--goal` rồi gọi adapter.
- `exercises/`: ba bài luyện tập về module, CLI và HTTP.
- `checks/check_week.py`: kiểm tra hành vi cốt lõi mà không gọi mạng.

## Chuẩn bị

Dùng Python 3.12 trở lên. Mở terminal tại thư mục gốc repository. Tuần này dùng thư viện chuẩn, không cần cài package ngoài để chạy các ví dụ.

## Chạy chương trình CLI

Từ thư mục gốc repository:

```bash
python weeks/week-13-modules-cli-api/cli.py --position 1 --goal 4
```

Kết quả dự kiến là một kết quả hành động có `right`, vì vị trí 1 còn ở trước mục tiêu 4. Thử đổi `--position` thành 4 để quan sát trường hợp đã tới mục tiêu.

Nếu thiếu một tham số bắt buộc hoặc nhập giá trị không phải số nguyên, `argparse` sẽ báo lỗi cách sử dụng.

## Làm các exercise

Chạy theo module mode từ thư mục gốc repository:

```bash
cd weeks/week-13-modules-cli-api
python -m exercises.ex01_modules
python -m exercises.ex02_cli --turn 3
python -m exercises.ex03_http
cd ../..
```

Module mode giúp Python tìm thấy package `bot_course` nằm cạnh thư mục `exercises`. Chi tiết xem [hướng dẫn exercises](exercises/README.md).

## Chạy self-check

Từ thư mục gốc repository:

```bash
python weeks/week-13-modules-cli-api/checks/check_week.py
```

Nếu mọi kiểm tra thành công, chương trình in:

```text
Week 13 solution checks: PASS
```

Self-check kiểm tra logic chọn hành động, tham số CLI, GET request, JSON hợp lệ và các trường hợp response lỗi. Nó chạy offline, không gửi request ra Internet và không gọi endpoint production của VuaCóc.

## Thứ tự học gợi ý

1. Đọc [notes](notes.md) và xem cấu trúc trong [bot_course](bot_course/).
2. Chạy `cli.py`, thay đổi tham số và quan sát kết quả.
3. Làm lần lượt [exercise 1](exercises/ex01_modules.py), [exercise 2](exercises/ex02_cli.py), [exercise 3](exercises/ex03_http.py).
4. Dùng [hints](hints.md) khi cần, rồi chạy self-check.
5. Xem [mini-project](mini-project/README.md) để ghép các khái niệm.

## Hoàn thành khi

- [ ] Giải thích được module khác package ở điểm nào.
- [ ] Giải thích được vì sao dùng main guard.
- [ ] Chạy được CLI với các giá trị khác nhau.
- [ ] Mô tả được ý nghĩa của status code và JSON response.
- [ ] Giải thích được vì sao các kiểm tra HTTP dùng fixture offline.
- [ ] Chạy self-check thành công và hiểu các assertion chính.

**Nguyên tắc:** học cách phân chia trách nhiệm và kiểm tra hành vi trước; chưa cần thêm framework hay gọi API thật.
