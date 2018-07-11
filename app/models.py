from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    access = db.Column(db.Boolean, default=False)
    picture = db.Column(db.String(160))

class Topic(db.Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship(Topic)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)

class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship(Question)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship(Topic)
    box = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

class Correction(db.Model):
    __tablename__ = 'correction'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship(Question)
    new_question = db.Column(db.String)
    new_answer = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
