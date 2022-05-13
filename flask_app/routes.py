# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from getpass import getuser
import re
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        # print("login failed")
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function


def getUser():
    return db.reversibleEncrypt('decrypt', session['email']) if 'email' in session else 'Unknown'
    # return session['email'] if 'email' in session else 'Unknown'


@app.route('/login')
def login():
    # print("login qccce")
    return render_template('login.html', user=getUser())


@app.route('/logout')
def logout():
    session.pop('email', default=None)
    return redirect('/')


@app.route('/processlogin', methods=["POST", "GET"])
def processlogin():
    form_fields = dict((key, request.form.getlist(
        key)[0]) for key in list(request.form.keys()))
    check1 = db.authenticate(
        email=form_fields['email'], password=form_fields['password'])
    if 'success' in check1 and check1['success'] == 1:
        session['email'] = db.reversibleEncrypt(
            'encrypt', form_fields['email'])
        return json.dumps({'success': 1})

    return json.dumps({'success': 0})


@app.route('/signup.html', methods=["POST"])
def signup():
    login_data = request.form
    print(login_data)
    lis = []
    for i in login_data.values():
        lis.append(i)
    db.createUser(lis[0], lis[1], lis[2])
    # get_data = db.get_feedback()
    return render_template('signup.html',  user=getUser())


#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())


@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    if (getUser() == "owner@email.com"):
        style = 'width: 100%;color:blue;text-align: right'
    else:
        style = 'width: 100%;color:red;text-align: left'
    emit('status', {'msg': getUser() +
         ' has entered the room.', 'style': style}, room='main')


@socketio.on('send-message', namespace='/chat')
def send_message(message):
    if (getUser() == "owner@email.com"):
        style = 'width: 100%;color:blue;text-align: right'
    else:
        style = 'width: 100%;color:red;text-align: left'
    emit('status1', {'msg': getUser() + ' said ' +
         message, 'style': style}, room='main')


@socketio.on('left', namespace='/chat')
def left(message):
    leave_room('main')
    if (getUser() == "owner@email.com"):
        style = 'width: 100%;color:blue;text-align: right'
    else:
        style = 'width: 100%;color:red;text-align: left'
    emit('status2', {'msg': getUser() +
         ' left the room. ', 'style': style}, room='main')


#######################################################################################
# WORDLE GAME
#######################################################################################

@app.route('/wordle.html')
@login_required
def wordle():
    return render_template('wordle.html', user=getUser())

#######################################################################################
# LEADERBOARD FOR WORDLE
#######################################################################################


@app.route('/processleaderboard', methods=['POST'])
def processleaderboard():
    form_fields = dict((key, request.form.getlist(
        key)[0]) for key in list(request.form.keys()))
    word = form_fields['response']
    time = form_fields['time']
    date = form_fields['date']
    db.send_leaderboard(getUser(), word, time, date)
    return {'success': 1}
    # return render_template('leaderboard.html', user=getUser())


@app.route('/leaderboard', methods=['POST'])
def leaderboard():
    data = db.get_leaderboard()
    return render_template("leaderboard.html", user=getUser(), lead_data = data)

@app.route('/leaderboard.html')
def leaderboard2():
    data = db.get_leaderboard()
    return render_template("leaderboard.html", user=getUser(),lead_data = data)
#######################################################################################
# OTHER
#######################################################################################


@app.route('/')
def root():
    return redirect('/home')


@app.route('/home')
def home():
    x = random.choice(
        ['I am from India', 'I like to work on Arduino', 'I like to travel'])
    return render_template('home.html', fun_fact=x, user=getUser())


@app.route('/home.html')
def home1():
    x = random.choice(
        ['I am from India', 'I like to work on Arduino', 'I like to travel'])
    return render_template('home.html', fun_fact=x, user=getUser())


@app.route('/projects.html')
def project():
    return render_template('projects.html', user=getUser())


@app.route('/piano.html')
def piano():
    return render_template('piano.html', user=getUser())


@app.route('/resume.html')
def resume():
    resume_data = db.getResumeData()
    return render_template('resume.html', resume_data=resume_data, user=getUser())


# @app.route('/processfeedback')
# def feedback():
# 	return render_template('processfeedback.html')

@app.route('/processfeedback.html', methods=['POST'])
def processfeedback():
    feedback_data = request.form
    db.send_feedback(feedback_data)
    get_data = db.get_feedback()
    return render_template('processfeedback.html', feedback=get_data, user=getUser())


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
