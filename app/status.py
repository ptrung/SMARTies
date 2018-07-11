from flask import session as login_session
from app import db
from app.models import User, Topic, Question, Status

def create_status(topic_name):
    topic = db.session.query(Topic).filter_by(name=topic_name).one()
    questions = db.session.query(Question).filter_by(topic=topic)
    user = db.session.query(User).filter_by(email=login_session['email']).one()
    for q in questions:
        newStatus = Status(question=q, topic=topic, box=1, user=user)
        db.session.add(newStatus)
        db.session.commit()
    return questions.count()

def update_status(status_id, box_new):
    status = db.session.query(Status).filter_by(id=status_id).one()
    status.box = box_new
    db.session.add(status)
    db.session.commit()

def exits_wrong_status(topic):
    status = db.session.query(Status).filter_by(topic=topic)
    count_status = status.count()
    count_correct_status = db.session.query(Status).filter_by(topic=topic).filter(Status.box > 0).filter(Status.box < 6).count()
    if count_correct_status == count_status:
        return False
    else:
        return True

def update_status_0_to_1_and_6_to_5():
    list_status = db.session.query(Status).all()
    for s in list_status:
        if s.box < 1 or s.box > 6:
            if s.box < 1:
                s.box = 1
            elif s.box > 5:
                s.box = 5
            db.session.add(s)
            db.session.commit()

def update_status_to_1(status_list):
    for s in status_list:
        update_status(s.id, 1)

def get_all_status():
    return db.session.query(Status).all()

def get_status_for_topic(topic):
    return db.session.query(Status).\
                       filter_by(topic=topic).\
                       filter_by(user_id=login_session['user_id'])

def get_status_for_box(topic, box):
    return db.session.query(Status).\
                   filter_by(topic=topic).\
                   filter_by(box=box).\
                   filter_by(user_id=login_session['user_id'])

def create_boxes(status):
    box_1 = status.filter_by(box=1).count()
    box_2 = status.filter_by(box=2).count()
    box_3 = status.filter_by(box=3).count()
    box_4 = status.filter_by(box=4).count()
    box_5 = status.filter_by(box=5).count()
    return (box_1, box_2, box_3, box_4, box_5)

def get_status_for_question(question):
    return db.session.query(Status).\
                filter_by(question=question).\
                filter_by(user_id=login_session['user_id']).one()
