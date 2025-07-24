from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify,session
from flask_login import login_required, current_user
from data.database import add_order, get_orders_by_user, cancel_order,get_cart, clear_cart, add_order


orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['GET', 'POST'])
def index():
    # LỖ HỔNG: Không có CSRF protection cho form POST
    message = None
    if session.get('logged_in'):
        user_id = session.get('user_id')
        if request.method == 'POST':
            name = request.form.get('name', '')
            address = request.form.get('address', '')
            phone = request.form.get('phone', '')
            # Tính tổng tiền mẫu (cố định 1 sản phẩm 25k)
            total_amount = 25000
            order_id = add_order(user_id, total_amount)
            if order_id:
                message = f"<div class='alert alert-success'>Cập nhật thành công! Cảm ơn <b>{name}</b>.</div>"
            else:
                message = f"<div class='alert alert-danger'>Cập nhật thất bại!</div>"
        orders = get_orders_by_user(user_id)
        return render_template('orders.html', message=message, orders=orders)
    else:
        return redirect(url_for('auth.login'))

@orders_bp.route('/cancel/<int:order_id>', methods=['POST'])
def cancel(order_id):
    # LỖ HỔNG: Không có CSRF protection
    if session.get('logged_in'):
        user_id = session.get('user_id')
        success = cancel_order(order_id, user_id)
        if success:
            flash('Đã hủy đơn hàng thành công!', 'success')
        else:
            flash('Không thể hủy đơn hàng này!', 'danger')
        return redirect(url_for('orders.index'))
    else:
        return redirect(url_for('auth.login'))

@orders_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # LỖ HỔNG: Không có CSRF protection cho form POST
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    user_id = session.get('user_id')
    cart_items = get_cart(user_id)
    if not cart_items:
        flash('Giỏ hàng trống!', 'warning')
        return redirect(url_for('carts.index'))
    total = sum(item[2] * item[3] for item in cart_items)
    if request.method == 'POST':
        name = request.form.get('name', '')
        address = request.form.get('address', '')
        phone = request.form.get('phone', '')
        total_amount = 25000
        order_id = add_order(user_id, total_amount)
        clear_cart(user_id)
        flash('Đặt hàng thành công!', 'success') 
        return redirect(url_for('orders.index'))   
    return redirect(url_for('orders.index'))
