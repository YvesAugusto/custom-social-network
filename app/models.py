from app import db, app
#import flask_whooshalchemyplus as wa

from sqlalchemy.ext.mutable import Mutable

class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value

class Usuario(db.Model):
    __searchable__ = ['first_name', 'last_name', 'id', 'email']
    __tablename__  = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(16))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(96), unique=True)
    sex = db.Column(db.String(6))
    city = db.Column(db.String(32))
    state = db.Column(db.String(32))
    password = db.Column(db.String(64))
    # vetor com o id dos usuarios seguidos
    seguindo = db.Column(MutableList.as_mutable(db.ARRAY(db.Integer)))
    # vetor com o id dos seguidores
    seguidores = db.Column(MutableList.as_mutable(db.ARRAY(db.Integer)))
    # vetor com as notificações de amizade que vão aparecer na página principal
    # cada elemento do vetor é o id da pessoa que enviou a solicitação
    invite_notifications = db.Column(MutableList.as_mutable(db.ARRAY(db.Integer)))

    def __init__(self, first_name, last_name, email,
                 sex, city, state, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.sex = sex
        self.city = city
        self.state = state
        self.password = password
        self.seguindo = []
        self.seguidores = []
        self.invite_notifications = []

    def seguir(self, id):
        self.seguindo.append(id)

    def receber_seguidor(self, id):
        self.seguidores.append(id)

    def unfollow(self, id):
        self.seguindo.remove(id)
    
    def be_unfollowed(self, id):
        self.seguidores.remove(id)

class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id')) # usuario que criou o post
    title = db.Column(db.String(32))
    content = db.Column(db.String(512))
    likes = db.Column(db.Integer)

    def __init__(self, user_id, title, content):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.likes = 0

    def like(self):
        self.likes+=1


class Commentary(db.Model):
    __tablename__='commentary'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.String(512))
    
    def __init__(self, user_id, post_id, content):
        self.user_id = user_id
        self.post_id = post_id
        self.content = content

class Chat(db.Model):
    __tablename__='chat'
    user_id_0 = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    user_id_1 = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    __table_args__=(
        db.PrimaryKeyConstraint(
            user_id_0, user_id_1
        ),
    )

    def __init__(self, user_0, user_1):
        self.user_id_0 = user_0
        self.user_id_1 = user_1

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    content = db.Column(db.String(512))

    def __init__(self, user_id, chat_id, content):
        self.user_id = user_id
        self.chat_id = chat_id
        self.content = content
    

#wa.whoosh_index(app, Usuario)

db.create_all()