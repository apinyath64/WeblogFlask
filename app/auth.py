from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import logout_user, login_user, login_required, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('เข้าสู่ระบบสำเร็จ', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('รหัสผ่านไม่ถูกต้อง กรุณากรอกข้อมูลใหม่อีกครั้ง', category='error')
        else:
            flash('ชื่อผู้ใช้ไม่ถูกต้อง กรุณากรอกข้อมูลใหม่อีกครั้ง', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        exist_email = User.query.filter_by(email=email).first()
        if user:
            flash('มีชื่อผู้ใช้นี้อยู่แล้ว', category='error')
        elif exist_email:
            flash('อีเมลนี้ถูกใช้งานแล้ว', category='error')
        elif password1 != password2:
            flash("รหัสผ่านไม่ตรงกัน!", category='error')
        elif len(password1) < 8:
            flash("รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร!", category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("สร้างบัญชีผู้ใช้สำเร็จ", category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
            

    return render_template("register.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('คุณออกจากระบบแล้ว', category='success')
    return redirect(url_for('auth.login'))