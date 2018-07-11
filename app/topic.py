from app import db
from app.models import User, Topic, Question, Status

def get_all_topics():
    return db.session.query(Topic).all()

def get_one_topic_by_name(topic_name):
    try:
        return db.session.query(Topic).filter_by(name=topic_name).one()
    except:
        return None

def create_new_topic(topic_name):
    newTopic= Topic(name=topic_name)
    db.session.add(newTopic)
    db.session.commit()
    return db.session.query(Topic).filter_by(name=topic_name).one()

def get_one_topic_by_id(topic_id):
    try:
        return db.session.query(Topic).filter_by(id=topic_id).one()
    except:
        return None

def update_topic(topic_id, topic_name):
    t = db.session.query(Topic).filter_by(id=topic_id).one()
    t.name = topic_name
    db.session.add(t)
    db.session.commit()

def delete_topic_by_id(topic_id):
    topic = db.session.query(Topic).filter_by(id=topic_id).one()
    status = db.session.query(Status).filter_by(topic=topic).delete()
    db.session.commit()
    question = db.session.query(Question).filter_by(topic=topic).delete()
    db.session.commit()
    db.session.delete(topic)
    db.session.commit()
