from flask import flash, redirect, render_template, url_for
from flask import session as login_session
from app import db
from app.models import User

def no_login():
    return redirect(url_for('auth.show_login'))

def no_permission():
    flash('Du hast keinen Zugriff auf diese Seite!')
    return redirect(url_for('show_topics'))

def no_access():
    flash('Du hast zurzeit keinen Zugriff. Fuer eine Freischaltung melde dich bitte bei einem Admin.')
    return render_template('base.html')

def create_user(login_session):
    stud = False;
    if login_session['email'].endswith("stud.sbg.ac.at"):
        stud = True;
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   is_admin=False,
                   access=stud,
                   picture=login_session['picture'])
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def get_userid(email):
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def is_admin():
    user = db.session.query(User).filter_by(email=login_session['email']).one()
    return user.is_admin

def has_access():
    user = db.session.query(User).filter_by(email=login_session['email']).one()
    return user.access

def update_admin(user_id, value):
    user = db.session.query(User).filter_by(id=user_id).one()
    user.is_admin = value
    db.session.add(user)
    db.session.commit()

def update_blocking(user_id, value):
    user = db.session.query(User).filter_by(id=user_id).one()
    user.access = value
    db.session.add(user)
    db.session.commit()

def get_all_user():
    return db.session.query(User).all()
