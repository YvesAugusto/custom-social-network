from app import db

class Usuario(db.Model):
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
    seguindo = db.Column(db.ARRAY(db.Integer, dimensions = 1))
    # vetor com o id dos seguidores
    seguidores = db.Column(db.ARRAY(db.Integer, dimensions = 1))

    def __init__(self, first_name, last_name, email,
                 sex, city, state, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.sex = sex
        self.city = city
        self.state = state
        self.password = password
    
    def seguir(self, id):
        self.seguindo.append(id)

    def receber_seguidor(self, id):
        self.seguidores.append(id)

class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id')) # usuario que criou o post
    title = db.Column(db.String(32))
    content = db.Column(db.String(512))
    comments = db.Column(db.ARRAY(db.String(128), dimensions = 1))
    likes = db.Column(db.Integer)

    def __init__(self, user_id, title, content):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.likes = 0

    def like(self):
        self.likes+=1
    
    def comment(self, commentary):
        self.comments.append(commentary)

class Timeline(db.Model):
    __tablename__='timeline'
    # id de um post qualquer
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    # id do usuario que vai receber o post na timeline
    receiver_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    __table_args__=(
        db.PrimaryKeyConstraint(
            post_id, receiver_id
        ),
    )

    def __init__(self, post_id, receiver_id):
        self.post_id = post_id
        self.receiver_id = receiver_id

db.create_all()