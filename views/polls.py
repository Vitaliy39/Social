from flask import Blueprint, render_template, request, session, redirect, url_for
from database.database import Database

poll_blueprint = Blueprint('polls', __name__)


@poll_blueprint.route('/<poll>', methods=['GET', 'POST'])
def index(poll):
    print(poll)
    if request.method == 'GET':
        return render_template('polls/poll_email.html')
    else:
        email = request.form.get('email')
        if email is not None:
            print(email)
            if Database.find_one(f'{poll}_answers', query={'email' : email}):
                return ('Второй раз запрещено')
            else:
                session['email'] = email
                questions = Database.find(collection=poll, query={})
                return redirect(url_for('polls.polling',email=email, poll=poll))
                #return render_template('polls/index.html', questions=questions)

@poll_blueprint.route('<poll>/<email>', methods=['GET', 'POST'])
def polling(email, poll):
    #print(email)
    coll_name = f'{poll}_answers'
    questions = Database.find(collection=poll, query={})
    if request.method == 'GET':
        questions = Database.find(collection=poll, query={})
        return render_template('polls/index.html', questions=questions)
    if request.method == 'POST':
        answers = {'email' : email}
        for question in list(questions):
            name = question['question']
            q_type = question['qtype']
            if q_type == 'text' or q_type == 'one':
                answ = request.form.get(question['question'])
                answers[name] = answ
            elif q_type == 'many':
                nums = question['nums']
                answ = []
                for i in range(int(nums)):
                    a = request.form.get(str(name) + str(i))
                    if a != None:
                        answ.append(a)
                answers[name] = answ
            elif q_type == 'table':
                height = int(question['height'])
                width = int(question['width'])
                answ = []
                for h in range(height):
                    row_question = question[f'answname{h}']
                    # for w in range(width):
                    # print(f'{row_question}')
                    a = request.form.get(f'{row_question}')
                    # print(a)
                    answ_dict = {row_question: a}
                    answ.append(answ_dict)
                answers[name] = answ
            #print(answers)
        session.pop('email')
        Database.insert(collection=coll_name, query=answers)
        return('Спасибо за прохождение опроса. Напоминаем, что опрос можно пройти только один раз.')

#@poll_blueprint.route('/answers/')
