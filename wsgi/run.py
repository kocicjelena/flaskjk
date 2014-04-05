from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template, abort
 
app = Flask(__name__)
 
app.config.from_pyfile('flaskjkapp.cfg')
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
 
@app.route('/')
@app.route('/hello')
def index():
    return "Hello from OpenShift"
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
            todo = Todo(request.form['title'], request.form['text'])
            db.session.add(todo)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('new.html') 
if __name__ == '__main__':
    app.run()