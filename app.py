from flask import Flask, render_template,session
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3

# Khởi tạo Flask app với đường dẫn template đúng
app = Flask(__name__, 
            template_folder='app/templates',
            static_folder='app/static')

# Cấu hình cơ bản
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/CTF/Juice-shop-python/data/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo SQLAlchemy
db = SQLAlchemy(app)

# Import và đăng ký các blueprints
from app.routes.auth import auth_bp
from app.routes.products import products_bp
from app.routes.orders import orders_bp
from app.routes.api import api_bp
from app.routes.carts import carts_bp
from app.routes.profile import profile_bp

# Đăng ký blueprints với URL prefix
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(carts_bp, url_prefix='/cart')
app.register_blueprint(profile_bp)

# Route trang chủ
@app.route('/')
def index():
    return render_template('index.html')

def run_init_sql():
    """Chạy script init.sql để thêm dữ liệu mẫu"""
    try:
        # Kiểm tra xem bảng products đã có dữ liệu chưa
        conn = sqlite3.connect('D:/CTF/Juice-shop-python/data/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"Database đã có {count} sản phẩm, bỏ qua việc import dữ liệu mẫu.")
            conn.close()
            return True
        
        # Đọc file init.sql
        with open('D:/CTF/Juice-shop-python/data/init.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Thực thi script
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        print("Đã import dữ liệu mẫu từ init.sql thành công!")
        return True
    except Exception as e:
        print(f"Lỗi khi import dữ liệu mẫu: {e}")
        return False

# Khởi tạo database
def init_database():
    from data.database import create_table, migrate_database
    print("🔄 Đang khởi tạo database...")
    
    # Tạo các bảng
    create_table()
    
    # Chạy script init.sql để thêm dữ liệu mẫu
    run_init_sql()
    
    print("✅ Database đã được khởi tạo thành công!")


if __name__ == '__main__':
    # Khởi tạo database
    init_database()
    # Xóa session cũ
    # Chạy app
    print("🚀 Khởi động Flask app...")
    app.run(debug=True, host='127.0.0.1', port=5000)
