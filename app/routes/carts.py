from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from data.database import get_cart, add_to_cart, remove_from_cart

carts_bp = Blueprint('carts', __name__)

@carts_bp.route('/', methods=['GET'])
def view_cart():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    user_id = session.get('user_id')
    cart_items = get_cart(user_id)
    total = sum(item[2] * item[3] for item in cart_items)
    return render_template('carts.html', cart_items=cart_items, total=total)

@carts_bp.route('/add', methods=['POST'])
def add_cart():
    # LỖ HỔNG: Không có CSRF protection
    if not session.get('logged_in'):
        flash('Bạn chưa đăng nhập!', 'danger')
        return redirect(url_for('auth.login'))
    user_id = session.get('user_id')
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    if not product_id:
        flash('Thiếu product_id!', 'danger')
        return redirect(url_for('products.list_products'))
    ok = add_to_cart(user_id, int(product_id), quantity)
    if ok:
        flash('Đã thêm vào giỏ hàng!', 'success')
    else:
        flash('Lỗi khi thêm vào giỏ hàng!', 'danger')
    return redirect(url_for('carts.view_cart'))

@carts_bp.route('/remove/<int:product_id>', methods=['POST'])
def remove_cart(product_id):
    # LỖ HỔNG: Không có CSRF protection
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    user_id = session.get('user_id')
    ok = remove_from_cart(user_id, product_id)
    if ok:
        flash('Đã xóa sản phẩm khỏi giỏ hàng!', 'success')
    else:
        flash('Lỗi khi xóa sản phẩm!', 'danger')
    return redirect(url_for('carts.view_cart'))

@carts_bp.route('/quick-checkout', methods=['POST'])
def quick_checkout():
    # LỖ HỔNG: Không có CSRF protection
    if not session.get('logged_in'):
        flash('Bạn chưa đăng nhập!', 'danger')
        return redirect(url_for('auth.login'))
    user_id = session.get('user_id')
    from data.database import get_cart, clear_cart, add_order
    cart_items = get_cart(user_id)
    if not cart_items:
        flash('Giỏ hàng của bạn đang trống!', 'danger')
        return redirect(url_for('carts.view_cart'))
    total = sum(item[2] * item[3] for item in cart_items)
    # Dữ liệu mặc định
    name = 'Customer'
    address = 'Thủ đức'
    phone = '08843434'
    order_id = add_order(user_id, total)
    if order_id:
        clear_cart(user_id)
        flash('Đặt hàng thành công!', 'success')
    else:
        flash('Đặt hàng thất bại!', 'danger')
    return redirect(url_for('orders.index')) 

@carts_bp.route('/count', methods=['GET'])
def cart_count():
    if not session.get('logged_in'):
        return jsonify({'count': 0})
    user_id = session.get('user_id')
    cart_items = get_cart(user_id)
    count = sum(item[3] for item in cart_items)  # item[3] là quantity
    return jsonify({'count': count}) 