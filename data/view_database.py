#!/usr/bin/env python3
"""
Script để xem các record trong database.db
"""

import sqlite3
from tabulate import tabulate

def view_database():
    """Xem tất cả record trong database"""
    try:
        # Kết nối database
        conn = sqlite3.connect('D:/CTF/Juice-shop-python/data/database.db')
        cursor = conn.cursor()
        
        print("🗄️  DATABASE VIEWER - Juice Shop Python")
        print("=" * 60)
        
        # 1. Xem cấu trúc bảng products
        print("\n📋 CẤU TRÚC BẢNG PRODUCTS:")
        print("-" * 40)
        cursor.execute("PRAGMA table_info(products)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        
        # 2. Xem số lượng record trong mỗi bảng
        print("\n📊 THỐNG KÊ SỐ LƯỢNG RECORD:")
        print("-" * 40)
        tables = ['users', 'products', 'orders', 'baskets']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table.upper()}: {count} records")
        
        # 3. Xem tất cả sản phẩm
        print("\n🍹 DANH SÁCH SẢN PHẨM:")
        print("-" * 40)
        cursor.execute("SELECT * FROM products ORDER BY id")
        products = cursor.fetchall()
        
        if products:
            headers = ['ID', 'Tên', 'Mô tả', 'Giá (VNĐ)', 'Stock', 'Image', 'Created At']
            # Cắt mô tả ngắn để dễ đọc
            formatted_products = []
            for product in products:
                desc = product[2][:50] + "..." if product[2] and len(product[2]) > 50 else product[2] or "N/A"
                formatted_products.append([
                    product[0],  # ID
                    product[1],  # Tên
                    desc,        # Mô tả (cắt ngắn)
                    f"{product[3]:,}" if product[3] else "N/A",  # Giá
                    product[4] or 0,  # Stock
                    product[5] or "N/A",  # Image
                    product[6][:10] if product[6] else "N/A"  # Created At
                ])
            
            print(tabulate(formatted_products, headers=headers, tablefmt="grid"))
        else:
            print("  Không có sản phẩm nào!")
        
        # 4. Xem tất cả users
        print("\n👥 DANH SÁCH USERS:")
        print("-" * 40)
        cursor.execute("SELECT id, username, email, created_at FROM users ORDER BY id")
        users = cursor.fetchall()
        
        if users:
            headers = ['ID', 'Username', 'Email', 'Created At']
            formatted_users = []
            for user in users:
                formatted_users.append([
                    user[0],  # ID
                    user[1],  # Username
                    user[2],  # Email
                    user[3][:10] if user[3] else "N/A"  # Created At
                ])
            
            print(tabulate(formatted_users, headers=headers, tablefmt="grid"))
        else:
            print("  Không có user nào!")
        
        # 5. Xem tất cả orders
        print("\n📦 DANH SÁCH ORDERS:")
        print("-" * 40)
        cursor.execute("SELECT * FROM orders ORDER BY id")
        orders = cursor.fetchall()
        
        if orders:
            headers = ['ID', 'User ID', 'Total Amount', 'Status', 'Created At']
            formatted_orders = []
            for order in orders:
                formatted_orders.append([
                    order[0],  # ID
                    order[1],  # User ID
                    f"{order[2]:,}" if order[2] else "N/A",  # Total Amount
                    order[3] or "N/A",  # Status
                    order[4][:10] if order[4] else "N/A"  # Created At
                ])
            
            print(tabulate(formatted_orders, headers=headers, tablefmt="grid"))
        else:
            print("  Không có order nào!")
        
        # 6. Xem tất cả baskets
        print("\n🛒 DANH SÁCH BASKETS:")
        print("-" * 40)
        cursor.execute("SELECT * FROM baskets ORDER BY id")
        baskets = cursor.fetchall()
        
        if baskets:
            headers = ['ID', 'User ID', 'Product ID', 'Quantity', 'Created At']
            formatted_baskets = []
            for basket in baskets:
                formatted_baskets.append([
                    basket[0],  # ID
                    basket[1],  # User ID
                    basket[2],  # Product ID
                    basket[3],  # Quantity
                    basket[4][:10] if basket[4] else "N/A"  # Created At
                ])
            
            print(tabulate(formatted_baskets, headers=headers, tablefmt="grid"))
        else:
            print("  Không có basket nào!")
        
        # 7. Kiểm tra field image của products
        print("\n🖼️  KIỂM TRA FIELD IMAGE:")
        print("-" * 40)
        cursor.execute("SELECT id, name, image FROM products ORDER BY id")
        image_check = cursor.fetchall()
        
        if image_check:
            headers = ['ID', 'Tên sản phẩm', 'Image Path']
            print(tabulate(image_check, headers=headers, tablefmt="grid"))
            
            # Kiểm tra đường dẫn
            print("\n🔍 PHÂN TÍCH ĐƯỜNG DẪN IMAGE:")
            for product in image_check:
                image_path = product[2]
                if image_path:
                    if image_path.startswith('/static/'):
                        print(f"  ✅ {product[1]}: Đường dẫn tương đối đúng")
                    elif image_path.startswith('D:/') or image_path.startswith('C:/'):
                        print(f"  ❌ {product[1]}: Đường dẫn tuyệt đối (cần sửa)")
                    else:
                        print(f"  ⚠️  {product[1]}: Đường dẫn không chuẩn")
                else:
                    print(f"  ❌ {product[1]}: Không có đường dẫn image")
        else:
            print("  Không có sản phẩm nào để kiểm tra!")
        
        conn.close()
        print("\n✅ Hoàn thành xem database!")
        
    except Exception as e:
        print(f"❌ Lỗi khi xem database: {e}")

def view_specific_table(table_name):
    """Xem record của một bảng cụ thể"""
    try:
        conn = sqlite3.connect('D:/CTF/Juice-shop-python/data/database.db')
        cursor = conn.cursor()
        
        print(f"\n📋 BẢNG {table_name.upper()}:")
        print("-" * 40)
        
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        
        if records:
            # Lấy tên cột
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            
            print(tabulate(records, headers=columns, tablefmt="grid"))
        else:
            print(f"  Không có record nào trong bảng {table_name}!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Lỗi khi xem bảng {table_name}: {e}")

def main():
    print("🗄️  DATABASE VIEWER")
    print("=" * 50)
    
    print("Chọn hành động:")
    print("1. Xem tất cả database")
    print("2. Xem bảng products")
    print("3. Xem bảng users")
    print("4. Xem bảng orders")
    print("5. Xem bảng baskets")
    print("6. Thoát")
    
    choice = input("\nNhập lựa chọn (1-6): ").strip()
    
    if choice == "1":
        view_database()
    elif choice == "2":
        view_specific_table("products")
    elif choice == "3":
        view_specific_table("users")
    elif choice == "4":
        view_specific_table("orders")
    elif choice == "5":
        view_specific_table("baskets")
    elif choice == "6":
        print("Tạm biệt!")
    else:
        print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main() 