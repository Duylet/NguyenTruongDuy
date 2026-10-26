# Tuần 14 — OOP Essentials, Composition và Inheritance

Tuần này học cách gom dữ liệu và hành vi liên quan vào object. Trọng tâm là thiết kế class có trách nhiệm rõ ràng, ưu tiên **composition** khi có thể thay thế một thành phần, và chỉ dùng **inheritance** khi quan hệ “is-a” thực sự hợp lý.

## Mục tiêu học tập

Sau tuần này, bạn có thể:

- phân biệt class và object;
- dùng `__init__`, `self`, instance attributes và methods;
- viết `__str__` để hiển thị object dễ đọc;
- kiểm tra dữ liệu đầu vào và báo lỗi bằng `ValueError`;
- dùng composition để một object ủy quyền công việc cho strategy;
- thay strategy mà không cần viết lại class `Bot`;
- nhận biết một ví dụ inheritance cơ bản qua quan hệ `Dog` là một `Animal`.

## Nội dung và thứ tự học

```text
class / object
      ↓
state + methods + responsibility
      ↓
composition: Bot + strategy có thể thay thế
      ↓
basic inheritance: Animal → Dog
```

- [`notes.md`](notes.md): khái niệm và ví dụ.
- [`examples/`](examples/): ví dụ minh họa.
- [`exercises/`](exercises/): ba bài thực hành.
- [`hints.md`](hints.md): gợi ý khi gặp khó khăn.
- [`checks/README.md`](checks/README.md): cách chạy machine check.
- [`mini-project/README.md`](mini-project/README.md): bài ghép kiến thức.

## Chạy các bài thực hành

Từ thư mục gốc repository:

```bash
python weeks/week-14-oop-essentials/exercises/ex01_classes.py
python weeks/week-14-oop-essentials/exercises/ex02_composition.py
python weeks/week-14-oop-essentials/exercises/ex03_inheritance.py
```

Các bài không yêu cầu cài thêm thư viện. Đọc code và thử thay dữ liệu đầu vào để hiểu hành vi, thay vì chỉ chạy một lần rồi chép kết quả.

### Bài 1 — Class và object

File `ex01_classes.py` định nghĩa `Progress` để lưu số phần việc đã hoàn thành và tổng số phần việc. Class kiểm tra rằng `total` phải dương và `completed` nằm trong khoảng hợp lệ; `percentage()` tính phần trăm, còn `__str__()` tạo dòng mô tả dễ đọc.

### Bài 2 — Composition

File `ex02_composition.py` định nghĩa `Bot`, nhận một strategy function. `choose_action()` ủy quyền việc chọn hành động cho strategy hiện tại. Hãy thử đổi `bot.strategy` từ `balanced` sang `defensive` và thay đổi vị trí đối thủ.

Trong ví dụ hiện tại, `balanced` và `aggressive` là strategy tối giản để minh họa cách thay thế; chúng chưa mô phỏng một hệ thống chiến đấu phức tạp.

### Bài 3 — Inheritance

File `ex03_inheritance.py` định nghĩa `Animal` với thuộc tính `name`, rồi cho `Dog` kế thừa thuộc tính đó và bổ sung method `speak()`. Đây là ví dụ nhỏ về quan hệ “is-a”, không phải lý do để dùng inheritance cho mọi trường hợp.

## Chạy machine check

Từ thư mục gốc repository:

```bash
python weeks/week-14-oop-essentials/checks/check_week.py
```

Nếu check thất bại, đọc thông báo lỗi và so sánh hành vi thực tế với điều kiện trong check. Không sửa check chỉ để làm cho nó báo thành công; hãy xác định yêu cầu mà code cần đáp ứng.

## Hoàn thành khi

- [ ] Giải thích được class, object, attribute và method.
- [ ] Nói được `self` tham chiếu đến object hiện tại như thế nào.
- [ ] Giải thích được các điều kiện kiểm tra của `Progress`.
- [ ] Giải thích được vì sao `Bot` nhận strategy thay vì tự chứa toàn bộ logic.
- [ ] Phân biệt được composition với inheritance.
- [ ] Chạy ba exercise và machine check, đồng thời hiểu kết quả.

## Phạm vi tuần này

Chỉ cần OOP cơ bản và một ví dụ inheritance dễ hiểu. Chưa cần multiple inheritance, metaclass, descriptor, framework kiến trúc hoặc design pattern nâng cao.

**Nguyên tắc:** chọn cách thiết kế đơn giản nhất vẫn diễn tả đúng trách nhiệm của chương trình.
