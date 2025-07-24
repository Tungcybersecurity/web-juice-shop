from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from data.database import update_profile

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/update-profile', methods=['GET', 'POST'],strict_slashes=False)
def profile():
    # LỖ HỔNG: Không có CSRF protection cho form POST
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        print("POST")
        name = request.form.get('name', '')
        address = request.form.get('address', '')
        phone = request.form.get('phone', '')
        session['profile_name'] = name
        session['profile_address'] = address
        session['profile_phone'] = phone
        # Lưu vào database
        username = session.get('username')
        if username:
            ok = update_profile(username, name, address, phone)
        else:
            flash('Không xác định được user!', 'danger')
        return redirect(url_for('profile.profile'))
    return render_template('profile.html',
        name=session.get('profile_name', ''),
        address=session.get('profile_address', ''),
        phone=session.get('profile_phone', ''),
        avatar=None) 