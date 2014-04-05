from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template, abort
from flaskext.mail import Mail
from flaskext.mail import Message 
app = Flask(__name__)
app.config.from_pyfile('run.cfg')
db = SQLAlchemy(app)
 
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('todo_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    done = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime)
 
    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.done = False
        self.pub_date = datetime.utcnow()
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
            todo = Todo(request.form['title'], request.form['text'])
            db.session.add(todo)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('new.html')
@app.route('/')
def index():
    return render_template('index.html',
        todos=Todo.query.order_by(Todo.pub_date.desc()).all()
    )	
@app.route('/todos/<int:todo_id>', methods = ['GET' , 'POST'])
def show_or_update(todo_id):
    todo_item = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template('view.html',todo=todo_item)
    todo_item.title = request.form['title']
    todo_item.text  = request.form['text']
    todo_item.done  = ('done.%d' % todo_id) in request.form
    db.session.commit()
    return redirect(url_for('index'))
@app.route("/email")
def email():
    msg = Message("Hello",
                  sender="kjelenak@hotmail.com",
                  recipients=["kocicjelena@gmail.com"])
	assert msg.sender == "Me <me@example.com>"
	mail.send(msg)
if __name__ == '__main__':
    app.run()