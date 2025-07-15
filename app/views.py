from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from .models import Post, Comment, User
from . import db

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return render_template("index.html")

@views.route("/home", methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'POST':
        content = request.form.get('content')

        if len(content) < 1:
            flash("ข้อความสั้นเกินไป", category='error')
        else:
            new_post = Post(content=content, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash("เพิ่มโพสต์สำเร็จ", category='success')

    posts = Post.query.order_by(desc(Post.created_at))

    return render_template("home.html", user=current_user, posts=posts)


@views.route("/posts", methods=["GET", "POST"])
@login_required
def get_all_post():
    posts = Post.query.all()
    return render_template("all_post.html", posts=posts, user=current_user)


@views.route("/posts/<int:post_id>", methods=["GET"])
@login_required
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', user=current_user, post=post)


@views.route("/posts/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        flash("คุณไม่สามารถแก้ไขโพสต์นี้ได้", category='error')
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        new_content = request.form.get('content')
        if new_content:
            post.content = new_content
            db.session.commit()
            flash("แก้ไขโพสต์สำเร็จ", category='success')
            return redirect(url_for('views.home'))
        else:
            flash("โพสต์ไม่สามารถว่างได้", category='error')

    return render_template('edit_post.html', user=current_user, post=post)


@views.route("/posts/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash("คุณไม่สามารถลบโพสต์นี้ได้", category='error')
    
    post.liked_by.clear()
    db.session.commit()

    db.session.delete(post)
    db.session.commit()
    flash("ลบโพสต์สำเร็จ", category='success')

    return redirect(url_for('views.home'))


@views.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    liked = False

    if current_user in post.liked_by:
        post.liked_by.remove(current_user)
    else:
        post.liked_by.append(current_user)
        liked = True
    db.session.commit()
        
    # return redirect(url_for('views.home'))
    return jsonify({
        'liked': liked,
        'like_count': len(post.liked_by)
    })
