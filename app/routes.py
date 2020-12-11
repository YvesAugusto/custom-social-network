from app import app, db
from flask import render_template, redirect, url_for
from flask import request, jsonify
from .validators import *
from .models import Usuario, Post, Timeline


@app.route('/controller/<id>/inviteFriend', methods=['POST'])
def inviteFriend(id):
    asking_user = Usuario.query.filter_by(id=id).first()
    print(asking_user.seguindo)
    receiving_user = Usuario.query.filter_by(id=request.form['id']).first()
    print(receiving_user)
    asking_user.seguir(receiving_user.id)
    db.session.commit()
    print(asking_user.seguindo)
    return {'error': 'followed'}

@app.route('/view/posts/<id>')
def get_user_timeline_posts(id):
    return 0

@app.route('/profile/<id>/post', methods=['POST'])
def make_post(id):
    content = request.form['content']
    title = request.form['title']
    post = Post(user_id=id, title=title, content=content)
    db.session.add(post)
    db.session.commit()
    return {'error':title}

@app.route('/login')
def login_page():
    return render_template("login.html")


@app.route('/login/controller', methods=['POST'])
def login_controller():
    email = request.form['email']
    password = request.form['password']
    if validate_email(email) and password:
        query = Usuario.query.filter_by(email=email).first()
        if query.password == password:
            return jsonify({'success': True, 'name':query.first_name + query.last_name, 'id':query.id})
    else:
        return jsonify({'error': 'missing data'})
    # render_template('./templates/login.html')

@app.route('/profile/<id>', methods=['POST', 'GET'])
def profile(id):
    usuario = Usuario.query.filter_by(id=id).first()
    posts= Post.query.filter_by(user_id=usuario.id).all()
    return render_template("timeline.html", posts=posts,
                            form={'username': usuario.first_name + " " + usuario.last_name,
                                'nickname': usuario.first_name + usuario.last_name})

@app.route('/enroll/user', methods=['GET', 'POST'])
def enroll_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    sex = request.form['sex']
    city = request.form['city']
    state = request.form['inputState']
    password = request.form['password']

    valid = first_name and last_name and validate_email(email) and city and state and password
    if valid:
        user = Usuario(first_name = first_name, last_name = last_name,
                       email = email, sex = sex, city = city,
                       state=state, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'error':'Sucessfully registered', 'type':'success'})
    else:
        return jsonify({'error':'Register failed', 'type':'danger'})

@app.route('/enroll', methods = ['GET'])
def enroll_page():
    return render_template("enroll.html")

@app.route('/profile/<id>/search')
def search(id):
    if request.method == 'GET':
        usuarios = Usuario.query.filter_by(first_name=request.args.get('first_name')).all()
    else:
        usuarios = []
    form={'username':Usuario.query.filter_by(id=id).first().first_name,
          'users': usuarios}
    return render_template('search_page.html', form=form)

@app.route('/views/<id>/usuario')
def view_usuario():
    usuarios = Post.query.whoosh_search(request.args.get('query')).all()
    form={'username':Usuario.query.filter_by(id=id).first().first_name,
          'users': usuarios}
    print(usuarios)
    return render_template('search_page.html', form=form)