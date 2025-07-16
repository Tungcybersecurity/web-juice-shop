#!/usr/bin/env python3
"""
Script để xóa hết record trong bảng products
"""

import sqlite3

def clear_products_table():
    """Xóa hết record trong bảng products"""
    try:
        # Kết nối database
        conn = sqlite3.connect('D:/CTF/Juice-shop-python/data/database.db')
        cursor = conn.cursor()
        
        # Đếm số record trước khi xóa
        cursor.execute("SELECT COUNT(*) FROM products")
        count_before = cursor.fetchone()[0]
        print(f"Số record hiện tại: {count_before}")
        
        if count_before == 0:
            print("Bảng products đã trống!")
            return
        
        # Xóa hết record
        cursor.execute("DELETE FROM products")
        
        # Reset auto-increment counter
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='products'")
        
        # Commit thay đổi
        conn.commit()
        
        # Đếm số record sau khi xóa
        cursor.execute("SELECT COUNT(*) FROM products")
        count_after = cursor.fetchone()[0]
        
        print(f"Đã xóa {count_before} record thành công!")
        print(f"Số record còn lại: {count_after}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Lỗi khi xóa record: {e}")
        return False

def reset_products_table():
    """Reset hoàn toàn bảng products (xóa và tạo lại)"""
    try:
        # Kết nối database
        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        
        # Xóa bảng cũ
        cursor.execute("DROP TABLE IF EXISTS products")
        
        # Tạo lại bảng
        create_table_sql = '''CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            stock INTEGER DEFAULT 0,
            image VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
        
        cursor.execute(create_table_sql)
        conn.commit()
        
        print("Đã reset hoàn toàn bảng products!")
        print("Bảng đã được tạo lại với schema mới.")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Lỗi khi reset bảng: {e}")
        return False

def main():
    print("🗑️  Script xóa record trong bảng products")
    print("=" * 50)
    
    print("Chọn hành động:")
    print("1. Xóa hết record (giữ lại bảng)")
    print("2. Reset hoàn toàn bảng (xóa và tạo lại)")
    print("3. Thoát")
    
    choice = input("Nhập lựa chọn (1-3): ").strip()
    
    if choice == "1":
        print("\n🔄 Đang xóa hết record...")
        if clear_products_table():
            print("✅ Hoàn thành!")
        else:
            print("❌ Có lỗi xảy ra!")
            
    elif choice == "2":
        print("\n⚠️  Cảnh báo: Hành động này sẽ xóa hoàn toàn bảng products!")
        confirm = input("Bạn có chắc chắn muốn tiếp tục? (y/N): ").strip().lower()
        
        if confirm == 'y':
            print("\n🔄 Đang reset bảng products...")
            if reset_products_table():
                print("✅ Hoàn thành!")
            else:
                print("❌ Có lỗi xảy ra!")
        else:
            print("Đã hủy thao tác.")
            
    elif choice == "3":
        print("Tạm biệt!")
        
    else:
        print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main() 