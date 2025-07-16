import sqlite3
from data.connect import get_connection
import bcrypt

database_name = 'database.db'
create_users_table_sql = '''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);'''

create_products_table_sql = '''CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);'''

create_orders_table_sql = '''CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);'''

create_baskets_table_sql = '''CREATE TABLE baskets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);'''

check_table_user_exists_sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='users';"
check_table_product_exist_sql="SELECT name FROM sqlite_master WHERE type='table' AND name='products';"
check_table_order_exist_sql="SELECT name FROM sqlite_master WHERE type='table' AND name='orders';"
check_table_basket_exist_sql="SELECT name FROM sqlite_master WHERE type='table' AND name='baskets';"
def create_table():
    """Create users table if it doesn't exist"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute(check_table_user_exists_sql)
        table_user_exists = cursor.fetchone()
        
        if not table_user_exists:
            cursor.execute(create_users_table_sql)
            conn.commit()
            print("Users table created successfully!")
        else:
            print("Users table already exists!")
        
        cursor.execute(check_table_product_exist_sql)
        table_products_exits= cursor.fetchone()

        if not table_products_exits:
            cursor.execute(create_products_table_sql)
            conn.commit()
            print("Products table created successfully!")
        else:
            print("Products table already exists!")
            # Check if image column exists, if not add it
            add_image_column_if_not_exists(cursor, conn)

        cursor.execute(check_table_order_exist_sql)
        table_orders_exists= cursor.fetchone()

        if not table_orders_exists:
            cursor.execute(create_orders_table_sql)
            conn.commit()
            print("Orders table created successfully!")
        else:
            print("Orders table already exists!")
        
        cursor.execute(check_table_basket_exist_sql)
        table_basket_exists= cursor.fetchone()

        if not table_basket_exists:
            cursor.execute(create_baskets_table_sql)
            conn.commit()
            print("Basket table created successfully!")
        else:
            print("Basket table already exists!")
            
        conn.close()
        
    except Exception as e:
        print(f"Error creating table: {e}")


# def init_database():
#     """Initialize database with sample data"""
#     with open('D:/CTF/Juice-shop-python/data/init.sql', 'r', encoding='utf-8') as f:
#         sql_script = f.read()

#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.executescript(sql_script)
#     conn.commit()
#     conn.close()
#     print("Đã import dữ liệu mẫu từ init.sql vào database.db")  

def add_image_column_if_not_exists(cursor, conn):
    """Add image column to products table if it doesn't exist"""
    try:
        # Check if image column exists
        cursor.execute("PRAGMA table_info(products)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'image' not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN image VARCHAR(255)")
            conn.commit()
            print("Image column added to products table successfully!")
        else:
            print("Image column already exists in products table!")
            
    except Exception as e:
        print(f"Error adding image column: {e}")

def migrate_database():
    """Run database migrations"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Add image column to products table if it doesn't exist
        add_image_column_if_not_exists(cursor, conn)
        
        conn.close()
        print("Database migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")


def add_new_user(username, password, email):
    """Add a new user to the database"""
    
    # Hash the password
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    insert_user_sql = '''INSERT INTO users (username, email, password_hash) 
                        VALUES (?, ?, ?)'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(insert_user_sql, (username, email, password_hash))
        conn.commit()
        
        print(f"User '{username}' added successfully!")
        conn.close()
        return True
        
    except sqlite3.IntegrityError as e:
        print(f"Error: Username or email already exists!")
        return False
    except Exception as e:
        print(f"Error adding user: {e}")
        return False
    

def get_password(username):
    get_password_sql = f'''select password_hash from users where username='{username}' '''

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(get_password_sql)
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return result[0]  # Trả về password_hash
        else:
            return None  # Không tìm thấy user
            
    except Exception as e:
        print(f"Error getting password: {e}")
        return None


def check_account(username, password):
    password_hash_from_database = get_password(username)
    
    if password_hash_from_database is None:
        return False  # User không tồn tại
    
    # So sánh password hash
    try:
        # Chuyển password_hash từ database về bytes để so sánh
        stored_hash_bytes = password_hash_from_database.encode('utf-8')
        
        # Kiểm tra password có match không
        is_match = bcrypt.checkpw(password.encode('utf-8'), stored_hash_bytes)
        
        return is_match
        
    except Exception as e:
        print(f"Error checking password: {e}")
        return False

def check_username_exists(username):
    """Kiểm tra username đã tồn tại chưa"""
    check_username_sql = f"SELECT username FROM users WHERE username='{username}'"
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(check_username_sql)
        result = cursor.fetchone()
        
        conn.close()
        
        return result is not None  # True nếu username đã tồn tại
        
    except Exception as e:
        print(f"Error checking username: {e}")
        return False

def check_email_exists(email):
    """Kiểm tra email đã tồn tại chưa"""
    check_email_sql = f"SELECT email FROM users WHERE email='{email}'"
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(check_email_sql)
        result = cursor.fetchone()
        
        conn.close()
        
        return result is not None  # True nếu email đã tồn tại
        
    except Exception as e:
        print(f"Error checking email: {e}")
        return False

def check_user_exists(username, email):
    """Kiểm tra user đã tồn tại chưa (username hoặc email)"""
    check_user_sql = f"SELECT username, email FROM users WHERE username='{username}' OR email='{email}'"
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(check_user_sql)
        result = cursor.fetchone()
        
        conn.close()
        
        return result is not None  # True nếu user đã tồn tại
        
    except Exception as e:
        print(f"Error checking user: {e}")
        return False


def get_all_products():
    """Get all products from database"""
    get_products_sql = "SELECT * FROM products ORDER BY created_at DESC"
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(get_products_sql)
        products = cursor.fetchall()
        
        conn.close()
        return products
        
    except Exception as e:
        print(f"Error getting products: {e}")
        return []

def get_product_by_id(product_id):
    """Get a specific product by ID"""
    get_product_sql = "SELECT * FROM products WHERE id = ?"
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(get_product_sql, (product_id,))
        product = cursor.fetchone()
        
        conn.close()
        return product
        
    except Exception as e:
        print(f"Error getting product: {e}")
        return None

def search_products(search_term):
    """Search products by name or description"""
    search_products_sql = '''SELECT * FROM products 
                            WHERE name LIKE ? OR description LIKE ?
                            ORDER BY created_at DESC'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{search_term}%"
        cursor.execute(search_products_sql, (search_pattern, search_pattern))
        products = cursor.fetchall()
        
        conn.close()
        return products
        
    except Exception as e:
        print(f"Error searching products: {e}")
        return [] 


