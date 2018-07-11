from flask import render_template, flash, redirect, url_for, request
from flask import session as login_session
from app import db
from app.main import bp
from app.models import User, Topic, Question, Status
from app.user import no_login, has_access, no_access
from app.topic import get_all_topics, get_one_topic_by_name
from app.status import exits_wrong_status, create_status, update_status
from app.status import create_boxes, get_status_for_box, get_status_for_topic
from app.status import update_status_to_1, update_status_0_to_1_and_6_to_5, get_status_for_question
from app.question import get_one_question_by_id
from app.correction import save_correction
from flask import render_template

@bp.route('/')
@bp.route('/index')
def index():
    t = get_all_topics()
    if 'username' not in login_session:
        return no_login()
    elif has_access():
        return render_template('showTopics.html', topics=t)
    else:
        return no_access()

@bp.route('/impressum')
def impressum():
    return render_template('impressum.html')

@bp.route('/topic/<path:topic_name>/')
def boxes(topic_name):
    if 'username' not in login_session:
        return no_login()
    elif has_access():
        topic = get_one_topic_by_name(topic_name)
        if exits_wrong_status(topic):
            update_status_0_to_1_and_6_to_5()
        status_of_topic = get_status_for_topic(topic)
        if status_of_topic.count() == 0:
            boxes = (create_status(topic_name), 0, 0, 0, 0)
        else:
            boxes = create_boxes(status_of_topic)

        return render_template('showBoxes.html', topic_name=topic_name, boxes=boxes)
    else:
        return no_access()

@bp.route('/topic/<path:topic_name>/box/<int:box>/question/', methods=['GET', 'POST'])
def show_question(topic_name, box):
    if 'username' not in login_session:
        return no_login()
    elif has_access():
        # change status for last question
        if request.method == 'POST':
            topic = get_one_topic_by_name(topic_name)
            status = get_status_for_box(topic, box).first()
            if 'correct' in request.form:
                f = int(box) + 1
            elif 'wrong' in request.form:
                f = 0
            update_status(status.id, f)

        # get new question
        topic = get_one_topic_by_name(topic_name)
        status = get_status_for_box(topic, box).first()
        if not status:
            update_status_0_to_1_and_6_to_5()
            return redirect(url_for('main.boxes', topic_name=topic.name))
        else:
            return render_template('showQuestion.html', topic=topic, question=status.question, box=box)
    else:
        return no_access()

@bp.route('/topic/<path:topic_name>/box/<int:box>/answer/')
def show_answer(topic_name, box):
    if 'username' not in login_session:
        return no_login()
    elif has_access():
        topic = get_one_topic_by_name(topic_name)
        status = get_status_for_box(topic, box).first()

        return render_template('showAnswer.html', topic=topic, question=status.question, box=box)
    else:
        return no_access()

@bp.route('/topic/<path:topic_name>/reset/')
def reset_topic(topic_name):
    if 'username' not in login_session:
        return no_login()
    elif has_access():
        topic = get_one_topic_by_name(topic_name)
        status = get_status_for_topic(topic).all()
        update_status_to_1(status)
        return redirect(url_for('main.boxes', topic_name=topic_name))
    else:
        return no_access()

@bp.route('/topic/<path:topic_name>/box/<int:box>/reset/')
def reset_questions(topic_name, box):
    if 'username' not in login_session:
        return no_login()
    elif has_access():
        topic = get_one_topic_by_name(topic_name)
        status = get_status_for_box(topic, box).all()
        update_status_to_1(status)
        return redirect(url_for('main.boxes', topic_name=topic_name))
    else:
        return no_access()

@bp.route('/topic/<path:topic_name>/show/')
def show_question_list(topic_name):
    if 'username' not in login_session:
        return no_login()
    elif has_access():
        topic = get_one_topic_by_name(topic_name)
        status = get_status_for_topic(topic).all()
        return render_template('showQuestionList.html', status=status, topic_name=topic_name)
    else:
        return no_access()

@bp.route('/question/<int:question_id>/correct', methods=['GET', 'POST'])
def correct_question(question_id):
    if 'username' not in login_session:
        return no_login()
    elif has_access():
        if request.method == 'POST':
            question = get_one_question_by_id(question_id)
            status = get_status_for_question(question)
            new_question = request.form['question']
            new_answer = request.form['answer']

            if new_question or new_answer:
                if new_question != question.question or new_answer != question.answer:
                    save_correction(question, new_question, new_answer)

            flash('Die Aenderung wird von einem Admin bearbeitet!')
            return redirect(url_for('main.show_question', topic_name=status.topic.name, box=status.box))
        else:
            question = get_one_question_by_id(question_id)
            return render_template('correctQuestion.html', question=question)
    else:
        return no_access()
