import sqlite3

DB_PATH = 'D:/CTF/Juice-shop-python/data/database.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Lấy danh sách tất cả các bảng
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    if table_name == 'sqlite_sequence':
        continue  # Không xóa bảng hệ thống này
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        print(f"Đã xóa bảng: {table_name}")
    except Exception as e:
        print(f"Lỗi khi xóa bảng {table_name}: {e}")

conn.commit()
conn.close()
print("Đã xóa toàn bộ bảng trong database.") 