import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

count = 1


# conn = psycopg2.connect(
#     host='localhost',
#     database='flask_project',
#     user='postgres',
#     password='0000')

# cur = conn.cursor()


# @app.route('/get-db')
# def get_db():
#     cur.execute('SELECT version()')
#     # show version
#     db_version = cur.fetchone()
#     print(db_version)

#     # close connection
#     cur.close()
#     return 'True'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    def __init__(self, title):
        self.title = title
        self.complete = False


@app.route('/')
@app.route('/<name>')
def home(name=None):
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run()
