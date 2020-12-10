from app import app, db
from flask import render_template
from flask import request, jsonify
from .validators import *
from .models import Usuario, Post, Timeline

@app.route('/view/posts/<id>')
def get_user_timeline_posts(id):
    return 0

@app.route('/profile/<id>/post', methods=['POST'])
def make_post(id):
    content = request.form['content']
    title = request.form['title']
    print(title)
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
    first_name = ""
    if len(request.form) > 0:
        searched_name = request.form['name']
        usuarios = Usuario.query.filter_by(first_name=searched_name).all()
        first_name = Usuario.query.filter_by(id = id).first().first_name

    return render_template("timeline.html", 
                            form={'username': usuario.first_name + " " + usuario.last_name,
                                  'nickname': usuario.first_name + usuario.last_name}, 
                            posts=posts, search={'name':first_name})

@app.route('/profile/<id>/search', methods=['POST', 'GET'])
def search_method(id):

    if request.method == 'POST':
        searched_name = request.form['name']
        usuarios = Usuario.query.filter_by(first_name=searched_name).all()
        first_name = Usuario.query.filter_by(id = id).first().first_name
        return {'names':usuarios}

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