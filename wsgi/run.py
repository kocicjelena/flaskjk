from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import TwilioRestClient
import twilio.twiml
import re
from twilio.util import TwilioCapability
from flask import Flask, request, flash, url_for, redirect, render_template, abort
from flask import make_response
app = Flask(__name__)
app.config.from_pyfile('run.cfg')
db = SQLAlchemy(app)
twilio_account_sid = "AC96c40c4506d9eb0ce591a72d0c75010a"
twilio_auth_token = "225cc2dccdd75b337b8755f71b95804e"
twilio_from_number = "+17047514524"
client = TwilioRestClient(twilio_account_sid, twilio_auth_token)
caller_id = "+381641797574"
callers = {
    "+2138934515": "nenny",
    "+17047514524": "ja",
}
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
@app.route("/cont", methods=['POST', 'GET'])
def cont():
    if request.method == ['POST']:
        client.sms.messages.create(
        to=request.form['phone_number'],
        from_=twilio_from_number,
        body="Check this out: %s?dl=false" % request.form['text'])
   
    return render_template('cont.html')
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
@app.route("/athome", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming requests."""
    from_number = request.values.get('From', None)
    if from_number in callers:
        caller = callers[from_number]
    else:
        caller = "Monkey"
 
    resp = twilio.twiml.Response()
    # Greet the caller by name
    resp.say("Hello " + caller)
    # Play an MP3
    resp.play("http://demo.twilio.com/hellomonkey/monkey.mp3")
 
    return str(resp)
@app.route('/calltemplate', methods=['GET', 'POST'])
def calltemplate():
    account_sid = "AC96c40c4506d9eb0ce591a72d0c75010a"
    auth_token  = "225cc2dccdd75b337b8755f71b95804e"
    client = TwilioRestClient(account_sid, auth_token)

    call = client.calls.create(to="+381641797574",
                           from_="+17047514524",
                           url="http://flaskjk-kjelenak.rhcloud.com/voice")
    print call.sid
@app.route('/template', methods=['GET', 'POST'])
def template():
    if request.method == 'POST':
        return "Hello" 
    return render_template('template.html')
@app.route('/voice', methods=['GET', 'POST'])
def voice():
    from_number = request.values.get('PhoneNumber', None)
 
    resp = twilio.twiml.Response()
 
    with resp.dial(callerId=caller_id) as r:
        # If we have a number, and it looks like a phone number:
        if from_number and re.search('^[\d\(\)\- \+]+$', from_number):
            r.number(from_number)
        else:
            r.client(default_client)
 
    return str(resp)
@app.route('/sms')
def sms():
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "AC96c40c4506d9eb0ce591a72d0c75010a"
    auth_token  = "225cc2dccdd75b337b8755f71b95804e"
    client = TwilioRestClient(account_sid, auth_token)
    #body = Todo.query.filter_by(title='1').first()
    message = client.sms.messages.create(body="Check this out" % Todo.query.filter_by(title='1').first(),
    to="+381641797574",    # Replace with your phone number
    from_="+17047514524") # Replace with your Twilio number
    print message.sid
    return 'Hello World'
@app.route('/client', methods=['GET', 'POST'])
def client():
    """Respond to incoming requests."""
 
    client_name = request.values.get('client', None) or "nenny"
 
    # Find these values at twilio.com/user/account
    account_sid = "AC96c40c4506d9eb0ce591a72d0c75010a"
    auth_token = "225cc2dccdd75b337b8755f71b95804e"
 
    capability = TwilioCapability(account_sid, auth_token)
 
    application_sid = "AP7f494fd198a91134a17c246fe398a913" # Twilio Application Sid
    capability.allow_client_outgoing(application_sid)
    capability.allow_client_incoming(client_name)
    token = capability.generate()
 
    return render_template('client.html', token=token,
                           client_name=client_name)
@app.route('/drugi')
def drugi():
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "AC96c40c4506d9eb0ce591a72d0c75010a"
    auth_token  = "225cc2dccdd75b337b8755f71b95804e"
    client = TwilioRestClient(account_sid, auth_token)
 
    message = client.sms.messages.create(body="pozdrav, , Jelena <3",
    to="+381691998796",    # Replace with your phone number
    from_="+17047514524") # Replace with your Twilio number
    print message.sid
    return 'Hello World'
if __name__ == '__main__':
    app.run()