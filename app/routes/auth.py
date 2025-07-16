from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from data.database import check_account, add_new_user
import sqlite3

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        # Kiểm tra đăng nhập bằng username hoặc email
        if username and check_account(username, password):
            # Tạo session để duy trì đăng nhập
            session['user_id'] = username
            session['username'] = username  # Lưu username để hiển thị
            session['logged_in'] = True
            session['remember'] = remember
            
            if remember:
                # Nếu chọn "remember me", session sẽ kéo dài hơn
                session.permanent = True
            
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('products.index'))
            
        elif email and check_account(email, password):
            # Tạo session để duy trì đăng nhập
            session['user_id'] = email
            session['username'] = email  # Lưu email làm username để hiển thị
            session['logged_in'] = True
            session['remember'] = remember
            
            if remember:
                session.permanent = True
            
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('products.index'))
        else:
            flash('Username/Email hoặc mật khẩu không đúng!', 'error')
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Mật khẩu không khớp!', 'error')
            return redirect(url_for('auth.register'))
        if not username or not email or not password:
            flash('Vui lòng điền đầy đủ thông tin!', 'error')
            return redirect(url_for('auth.register'))
        if add_new_user(username, password, email):
            flash('Đăng ký thành công!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Đăng ký thất bại!', 'error')
            return redirect(url_for('auth.register'))
        
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    # Xóa session
    session.clear()
    flash('Bạn đã đăng xuất thành công!', 'success')
    return redirect(url_for('products.index'))

