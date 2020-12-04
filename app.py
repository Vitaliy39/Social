from flask import Flask
from views.users import user_blueprint
from views.polls import poll_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint, url_prefix='/')
app.register_blueprint(poll_blueprint, url_prefix='/poll')
app.secret_key = 'mysecretkey'

#@app.route('/')
#def index():
#    return('hello')

if __name__ == '__main__':
    app.run(debug=False)