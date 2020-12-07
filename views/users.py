from flask import Blueprint, render_template, request, url_for, session, redirect, send_file
from database.database import Database
import copy
import json
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

user_blueprint = Blueprint('user', __name__)
ADDRESS = 'https://socialbfu.herokuapp.com/'


@user_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')
    if request.method == 'POST':
        if request.form['login']:
            email = request.form.get('email')
            password = request.form.get('password')
            user = Database.find_one('users', {'email': email})
            if user:
                print(user)
                if check_password_hash(user['password'], password):
                    print('OK')
                    session['email'] = user['email']
                    return redirect(url_for('user.list'))
                else:
                    return ('Неправильное имя пользователя или пароль')
            else:
                return ('Неправильное имя пользователя или пароль')
    return render_template('users/login.html')


@user_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return (render_template('users/register.html', message='Введете свою электронную почту и пароль'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))
        user = Database.find_one('users', {'email': email})
        if user:
            return (render_template('users/register.html', message='Данный пользователь уже существует'))
        else:
            Database.insert('users', {'email': email, 'password': password, 'collections': [{}]})
            return redirect(url_for('user.login'))


@user_blueprint.route('/<item>/<question>')
def delete_question(item, question):
    if (request.method == 'GET') and ('email' in session):
        questions = Database.find(collection=item, query={})
        for i in questions:
            if (str(i) == str(question)):
                Database.delete(collection=item, query=i)
        return (render_template('users/questions_test.html', questions=questions, item=item, address=ADDRESS))
    else:
        return ('Вы не авторизованы')


@user_blueprint.route('/list/<item>', methods=['GET', 'POST'])
def delete_collection(item):
    if 'email' in session:
        user = Database.find_one('users', {'email': session['email']})
        if request.method == 'GET':
            new_user = copy.deepcopy(user)
            for i in new_user['collections']:
                if (str(i) == str(item)):
                    new_user['collections'].remove(i)
            Database.update(collection='users', query=user, data=new_user)
            try:
                return render_template('users/list.html', email=(session['email']), collections=user['collections'])
            except:
                return render_template('users/list.html', email=(session['email']), collections=[])


@user_blueprint.route('/list/', methods=['GET', 'POST'])
def list():
    if 'email' in session:
        user = Database.find_one('users', {'email': session['email']})
        if request.method == 'GET':
            try:
                return render_template('users/list.html', email=(session['email']), collections=user['collections'])
            except:
                return render_template('users/list.html', email=(session['email']), collections=[])

        if request.method == 'POST':
            new_name = request.form.get('newcollection')
            new_description = request.form.get('newdescription')
            new_collection = {'name': new_name, 'description': new_description}
            new_user = copy.deepcopy(user)
            if new_user['collections']:
                new_user['collections'].append(new_collection)
            else:
                new_user['collections'] = []
                new_user['collections'].append(new_collection)
            Database.update(collection='users', query=user, data=new_user)
            return render_template('users/list.html', email=(session['email']), collections=user['collections'])
    else:
        return 'Вы не авторизованы'


@user_blueprint.route('/answer/<answer>', methods=['GET', 'POST'])
def answers(answer):
    answers_collection = f'{answer}_answers'
    answers = Database.find(collection=answers_collection, query={})
    if request.method == 'GET':
        return render_template('users/answer.html', answer=answer, answers=answers, address=ADDRESS)
    if request.method == 'POST':
        with open(f'{answers_collection}.txt', 'w', encoding='utf-8') as f:
            for i in answers:
                i.pop('_id')
                f.write(json.dumps(i, ensure_ascii=False))
                f.write('\n')
        return send_file(f'{answers_collection}.txt', as_attachment=True)


@user_blueprint.route('/<item>/', methods=['GET', 'POST'])
def questions(item):
    if (request.method == 'GET') and ('email' in session):
        questions = Database.find(collection=item, query={})
        return (render_template('users/questions_test.html', questions=questions, item=item, address=ADDRESS))
    else:
        return ('Вы не авторизованы')


@user_blueprint.route('/add/<item>/', methods=['GET', 'POST'])
def add(item):
    types = ['table', 'one', 'many', 'text']
    params = request.args.to_dict()
    # print(len(params))
    # (params)
    if (len(params) > 1):
        try:
            if params['selectq'] == 'table':
                # print(params)
                return render_template('users/add_table.html', params=params)
            if params['selectq'] == 'text':
                data = dict(params)
                data['qtype'] = data['selectq']
                del data['selectq']
                Database.insert(collection=item, query=data)
                return render_template('users/add.html', types=types)
            else:
                return render_template('users/add_variant.html', params=params)
        except:
            print(params)
            if params['qtype']:
                data = dict(params)
                print(data)
                Database.insert(collection=item, query=data)
                return (render_template('users/add.html', item=item, types=types))
    return render_template('users/add.html', types=types)


@user_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email')
    return redirect(url_for('user.login'))


@user_blueprint.route('/create_table/', methods=['GET', 'POST'])
def create_table(params):
    return render_template('questions/add_table.html', params=params)


def delete(params):
    print(params)
