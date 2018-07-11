from flask import session as login_session
from app import db
from app.models import Correction, User

def save_correction(question, new_question, new_answer):
    user = db.session.query(User).filter_by(email=login_session['email']).one()
    newCorrection = Correction(question=question, new_question=new_question, new_answer=new_answer, user=user)
    db.session.add(newCorrection)
    db.session.commit()

def get_corrections_for_question(question):
    return db.session.query(Correction).filter_by(question=question).all()

def delete_correction_by_id(correction_id):
    correction = db.session.query(Correction).filter_by(id=correction_id).one()
    db.session.delete(correction)
    db.session.commit()

def get_all_corrections():
    try:
        return db.session.query(Correction).all()
    except:
        return None
