from flask import render_template, redirect, request
from flask_login import login_user, logout_user, current_user, login_required

from .db import User, db, Post, Comment
from .forms import RegistrationForm
from .settings import app, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@login_required
def main():
    request.args['id']  # 1
    return render_template('main.html', user=current_user)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()  # None
        if user is None or user.password != password:
            return render_template('login.html', msg='Invalid username or password')
        remember_me = bool(request.form.get('remember_me'))
        login_user(user, remember=remember_me)
        return redirect('/')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/posts')
@login_required
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)


@app.route('/create_comment/<int:id>', methods=["POST"])
@login_required
def create_comment(id):
    comment = Comment(user=current_user.id, post=id, text=request.form['comment'])
    db.session.add(comment)
    db.session.commit()
    return redirect(f'/post/{id}')

# Видалення коментарів
@app.route('/post/<int:id>')
def post(id):
    p = Post.query.get(id)
    user = User.query.get(p.user)
    comments = Comment.query.filter_by(post=id)
    return render_template('post.html', post=p, user=user, comments=comments)


@app.route('/edit-post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        post.text = request.form['text']
        db.session.commit()
        return redirect(f'/post/{post.id}')
    return render_template('edit_post.html', post=post)


@app.route('/delete-post/<int:id>', methods=['GET', 'POST'])
def delete_post(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    return render_template('delete_post.html', post=post)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        text = request.form['text']
        post = Post(text=text, user=1)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    return render_template('add_post.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/edit-profile', methods=['POST'])
@login_required
def edit_profile():
    # {'name':, 'status':, 'age':}
    current_user.username = request.form['name']
    current_user.status = request.form['status']
    current_user.age = request.form['age']
    db.session.commit()
    return redirect('/profile')
