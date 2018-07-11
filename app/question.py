from app import db
from app.models import Question, Status

def update_question(question_id, question, answer):
    f = db.session.query(Question).filter_by(id=question_id).one()
    f.question = question
    f.answer = answer
    db.session.add(f)
    db.session.commit()

def get_all_question():
    return db.session.query(Question).all()

def get_one_question_by_id(question_id):
    return db.session.query(Question).filter_by(id=question_id).one()

def get_all_questions_of_topic(topic):
    return db.session.query(Question).filter_by(topic=topic).all()

def add_questions_from_dict(dict, topic):
    for q,a in zip(dict['question'], dict['answer']):
        newQuestion = Question(topic=topic, question=q, answer=a)
        db.session.add(newQuestion)
        db.session.commit()

def delete_question_by_id(question_id):
    question = db.session.query(Question).filter_by(id=question_id).one()
    status = db.session.query(Status).filter_by(question=question).delete()
    db.session.commit()
    db.session.delete(question)
    db.session.commit()
