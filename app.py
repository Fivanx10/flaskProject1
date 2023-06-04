import flask
from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user="postgres",
        password="1234"
    )
    return conn


class SubscriptionForm(FlaskForm):
    name = StringField('Имя')
    email = StringField('Почта')
    submit = SubmitField('Отправить')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Don\'t think about this'


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "books";')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)


@app.route('/dosearch')
def dosearch():
    return render_template('dosearch.html')


@app.route('/getsearch/')
def get_search_view():
    mail = flask.request.args.get('mail')
    return f'Это страница поиска, параметр передан через get. Выполняется поиск по "{mail}"'


@app.route('/postsearch/', methods=['POST'])
def post_search_view():
    mail = flask.request.form.get('mail')
    return f'Это страница поиска, параметр передан через post. Выполняется поиск по "{mail}"'


@app.route('/subscribe/', methods=['GET','POST'])
def subscribe_view():
    form = SubscriptionForm()

    if flask.request.method == "GET":
        return render_template('subscribe.html', form=form)

    return '{}{}'.format(form.name.data, form.email.data)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    (title, author, pages_num, review))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == '__main__':
    app.run()
