from app import app, db
from flask import render_template, redirect, url_for
from flask import request, jsonify
from .validators import *
from .models import Usuario, Post, Timeline

@app.route('/controller/<id>/deleteFriend', methods=['POST'])
def deleteFriend(id):
    # query to get the current user logged on the social net
    current_user = Usuario.query.filter_by(id=id).first()
    # transform the string 'unmake_id' on a integer 'id' to search on the tables
    id_target = int(request.form['id'].split('_')[-1])
    # query user that will be removed from friendlist
    user_to_be_removed_from_friendlist = Usuario.query.filter_by(id=id_target).first()
    # manually set the new following vector
    seguindo = current_user.seguindo.copy()
    seguindo.remove(user_to_be_removed_from_friendlist.id)
    current_user.seguindo = seguindo
    # manually set the new followers vector
    seguidores = current_user.seguidores.copy()
    seguidores.remove(user_to_be_removed_from_friendlist.id)
    current_user.seguidores = seguidores
    db.session.add(current_user)

    # # --------------------------------------------

    # manually set the new following vector
    seguindo = user_to_be_removed_from_friendlist.seguindo.copy()
    seguindo.remove(current_user.id)
    user_to_be_removed_from_friendlist.seguindo = seguindo
    # manually set the new followers vector
    seguidores = user_to_be_removed_from_friendlist.seguidores.copy()
    seguidores.remove(current_user.id)
    user_to_be_removed_from_friendlist.seguidores = seguidores
    db.session.add(user_to_be_removed_from_friendlist)

    # # ---------------------------------------------

    db.session.commit()
    db.session.close()

    return {'error': 'unfollowed'}

@app.route('/controller/<id>/inviteFriend', methods=['POST'])
def inviteFriend(id):
    asking_user = Usuario.query.filter_by(id=id).first()
    id_target = int(request.form['id'].split('_')[-1])
    receiving_user = Usuario.query.filter_by(id=id_target).first()
    print(f'asking user following: {asking_user.seguindo}, and being followed by: {asking_user.seguidores}')
    asking_user.seguir(receiving_user.id)
    asking_user.receber_seguidor(receiving_user.id)
    print(f'asking user following: {asking_user.seguindo}, and being followed by: {asking_user.seguidores}')
    print()
    print(f'receiving user following: {receiving_user.seguindo}, and being followed by: {receiving_user.seguidores}')
    receiving_user.seguir(asking_user.id)
    receiving_user.receber_seguidor(asking_user.id)
    print(f'receiving user following: {receiving_user.seguindo}, and being followed by: {receiving_user.seguidores}')
    db.session.commit()
    db.session.close()
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
    usuario = Usuario.query.filter_by(id=id).first()
    if request.method == 'GET':
        usuarios = Usuario.query.filter_by(first_name=request.args.get('first_name')).all()
    else:
        usuarios = []
    form={'username':Usuario.query.filter_by(id=id).first().first_name,
          'users': usuarios, 'friends':usuario.seguindo}
    return render_template('search_page.html', form=form)

@app.route('/views/<id>/usuario')
def view_usuario():
    usuarios = Post.query.whoosh_search(request.args.get('query')).all()
    form={'username':Usuario.query.filter_by(id=id).first().first_name,
          'users': usuarios}
    return render_template('search_page.html', form=form)