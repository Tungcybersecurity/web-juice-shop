from flask import Blueprint, render_template, request, jsonify, session
from data.database import get_all_products, search_products, get_product_by_id
import sqlite3

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def index():
    # Kiểm tra xem user đã đăng nhập chưa
    if session.get('logged_in'):
        # Nếu đã đăng nhập, render template cho user
        print("Đã đăng nhập")
        return render_template('index_user.html')
    else:
        print("Chưa đăng nhập")
        # Nếu chưa đăng nhập, render template cho guest
        return render_template('index.html')

@products_bp.route('/all-protducs', methods=['GET', 'POST'],strict_slashes=False)
def list_products():
    """Hiển thị danh sách sản phẩm"""
    search_term = request.args.get('search')
    print(search_term)
    if search_term:
        products = search_products(search_term)
        print(products)
    else:
        products = get_all_products()
    
    if session.get('logged_in'):
        return render_template('products_user.html', products=products)
    else:
        return render_template('products.html', products=products)

@products_bp.route('/detail-products/<int:product_id>')
def product_detail(product_id):
    """Trả về chi tiết sản phẩm dưới dạng JSON"""
    product = get_product_by_id(product_id)
    
    if product:
        # Chuyển đổi product thành dictionary
        product_data = {
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],                        
            'stock': product[4],
            'image': product[6] if product[6] else '/static/images/orange-juice.jpg', # nếu theo như bảng trong database.py thì cột image là product[5] và create_at là product[6]
            'created_at': product[5] if len(product) > 6 else None
        }
        return jsonify(product_data)
    else:
        return jsonify({'error': 'Sản phẩm không tồn tại'}), 404

@products_bp.route('/view/<int:product_id>')
def view_product(product_id):
    product = get_product_by_id(product_id)
    if product:
        return render_template('product_detail.html', product=product)
    else:
        return render_template('404.html'), 404

@products_bp.route('/api/products')
def api_products():
    """API endpoint để lấy danh sách sản phẩm"""
    search_term = request.args.get('search')
    
    if search_term:
        products = search_products(search_term)
    else:
        products = get_all_products()
    
    # Chuyển đổi thành JSON
    products_list = []
    for product in products:
        products_list.append({
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],
            'stock': product[4],
            'image': product[5],
            'created_at': product[6]
        })
    
    return jsonify(products_list)

@products_bp.route('/api/products/<int:product_id>')
def api_product_detail(product_id):
    """API endpoint để lấy chi tiết sản phẩm"""
    product = get_product_by_id(product_id)
    
    if product:
        return jsonify({
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],
            'stock': product[4],
            'image': product[5],
            'created_at': product[6]
        })
    else:
        return jsonify({'error': 'Product not found'}), 404

