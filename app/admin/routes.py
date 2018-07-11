from flask import render_template, redirect, url_for, flash, request, Response
from flask import session as login_session
from app.user import no_login, no_permission, get_all_user, is_admin, update_admin, update_blocking
from app.status import get_all_status
from app.question import get_all_question, get_one_question_by_id
from app.question import update_question, get_all_questions_of_topic
from app.question import delete_question_by_id, add_questions_from_dict
from app.topic import get_all_topics, get_one_topic_by_name, create_new_topic
from app.topic import get_one_topic_by_id, update_topic, delete_topic_by_id
from app.admin import bp
from app.models import User, Question, Status, Topic
from app.admin.csvhandler import csv_file_to_dict, questions_to_csv_file
from app.correction import get_corrections_for_question, get_all_corrections, delete_correction_by_id
import io, csv

@bp.route('/')
def admin():
    if 'email' not in login_session:
        return no_login()
    elif is_admin():
        return render_template('admin/admin.html')
    else:
        return no_permission()

@bp.route('/users/')
def show_users():
    if 'email' not in login_session:
        return no_login()
    elif is_admin():
        u = get_all_user()
        return render_template('admin/showUsers.html', liste=u)
    else:
        return no_permission()

@bp.route('/user/<int:user_id>/admin', methods=['POST'])
def update_user_admin(user_id):
    if is_admin():
        if 'admin' in request.form:
            update_admin(user_id, True)
        elif 'noadmin' in request.form:
            update_admin(user_id, False)
    return redirect(url_for('admin.show_users'))

@bp.route('/user/<int:user_id>/access', methods=['POST'])
def update_access(user_id):
    if is_admin():
        if 'block' in request.form:
            update_blocking(user_id, False)
        elif 'free' in request.form:
            update_blocking(user_id, True)
    return redirect(url_for('admin.show_users'))

@bp.route('/status/')
def show_status():
    if 'email' not in login_session:
        return no_login()
    elif is_admin():
        s = get_all_status()
        return render_template('admin/showStatus.html', liste=s)
    else:
        return no_permission()

@bp.route('/questions', methods=['GET', 'POST'])
def questions():
    if 'username' not in login_session:
        return no_login()
    elif is_admin():
        if request.method == 'GET':
            question = get_all_question()
            topics = get_all_topics()
            return render_template('admin/showQuestions.html', question=question, topics=topics)
        else:
            # TODO: Filter
            question = get_all_question()
            topics = get_all_topics()
            return render_template('admin/showQuestions.html', question=question, topics=topics)
    else:
        return no_permission()

@bp.route('/questions/topic/<path:topic_name>/')
def topic_questions(topic_name):
    if 'username' not in login_session:
        return no_login()
    elif is_admin():
        topic = get_one_topic_by_name(topic_name)
        if topic == None:
            return redirect(url_for('admin.questions'))
        else:
            question = get_all_questions_of_topic(topic)
            topics = get_all_topics()
            return render_template('admin/showQuestions.html', question=question, topics=topics)
    else:
        return no_permission()

@bp.route('/questions/add', methods=['GET', 'POST'])
def add_questions():
    if 'username' not in login_session:
        return no_login()
    elif is_admin():
        if request.method == 'GET':
            topic = get_all_topics()
            return render_template('admin/addQuestions.html', topic=topic)
        else:
            if 'file' not in request.files:
                flash('Sie muessen ein File auswaehlen')
                return redirect(request.url)
            file = request.files['file']

            topic_name = request.form['topic']
            topic = get_one_topic_by_name(topic_name)
            if topic == None:
                topic = create_new_topic(topic_name)

            questions = csv_file_to_dict(file)
            add_questions_from_dict(questions, topic)

            return redirect(url_for('admin.topic_questions', topic_name=topic_name))
    else:
        return no_permission()

@bp.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    if 'username' not in login_session:
        return no_login()
    elif is_admin():
        if request.method == 'GET':
            question = get_one_question_by_id(question_id)
            return render_template('admin/question.html', question=question)
        else:
            update_question(question_id, request.form['question'], request.form['answer'])
            question = get_one_question_by_id(question_id)
            return render_template('admin/question.html', question=question)
    else:
        return no_permission()

@bp.route('/question/<int:question_id>/edit')
def edit_question(question_id):
    if 'username' not in login_session:
        return no_login()
    elif is_admin():
        question = get_one_question_by_id(question_id)
        corrections = get_corrections_for_question(question)
        return render_template('admin/editQuestion.html', question=question, corrections=corrections)
    else:
        return no_permission()

@bp.route('/question/<int:question_id>/delete')
def delete_question(question_id):
    if 'username' not in login_session:
        return no_login()
    elif is_admin():
        delete_question_by_id(question_id)
        return redirect(url_for('admin.questions'))
    else:
        return no_permission()

@bp.route('/topics', methods=['GET', 'POST'])
def topics():
    if 'username' not in login_session:
        return no_login()
    elif is_admin():
        if request.method == 'GET':
            topics = get_all_topics()
            return render_template('admin/showTopics.html', topics=topics)
        else:
            # TODO: Filter
            topics = get_all_topics()
            return render_template('admin/showTopics.html', topics=topics)
    else:
        return no_permission()

@bp.route('/topic/<int:topic_id>/edit', methods=['GET', 'POST'])
def edit_topic(topic_id):
    if 'username' not in login_session:
        return no_login()
    elif is_admin():
        if request.method == 'GET':
            topic = get_one_topic_by_id(topic_id)
            return render_template('admin/editTopic.html', topic=topic)
        else:
            update_topic(topic_id, request.form['topic'])
            return redirect(url_for('admin.topics'))
    else:
        return no_permission()

@bp.route('/topic/<int:topic_id>/delete')
def delete_topic(topic_id):
    if 'username' not in login_session:
        return no_login()
    elif is_admin():
        delete_topic_by_id(topic_id)
        return redirect(url_for('admin.topics'))
    else:
        return no_permission()

@bp.route('/topic/<int:topic_id>/export')
def export_topic(topic_id):
    if 'username' not in login_session:
        return no_login()
    elif is_admin():
        topic = get_one_topic_by_id(topic_id)
        questions = get_all_questions_of_topic(topic)
        si = io.BytesIO()
        cw = csv.writer(si, delimiter=';')
        cw.writerow(('question','answer'))
        for q in questions:
            cw.writerow((q.question.encode('utf-8'),q.answer.encode('utf-8')))

        return Response(
            si.getvalue().strip('\r\n'),
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename="+topic.name+".csv"})
    else:
        return no_permission()

@bp.route('/corrections', methods=['GET', 'POST'])
def corrections():
    if 'username' not in login_session:
        return no_login()
    elif is_admin():
        if request.method == 'GET':
            corrections = get_all_corrections()
            return render_template('admin/showCorrections.html', corrections=corrections)
        else:
            # TODO: Filter
            corrections = get_all_corrections()
            return render_template('admin/showCorrections.html', corrections=corrections)
    else:
        return no_permission()

@bp.route('/question/<int:question_id>/correction/<int:correction_id>/delete')
def delete_correction(question_id, correction_id):
    if 'username' not in login_session:
        return no_login()
    elif is_admin():
        delete_correction_by_id(correction_id)
        return redirect(url_for('admin.edit_question', question_id=question_id))
    else:
        return no_permission()
