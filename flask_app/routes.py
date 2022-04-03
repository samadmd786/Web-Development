# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request
from .utils.database.database  import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
db = database()

@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x     = random.choice(['I am from India','I like to work on Arduino','I like to travel'])
	return render_template('home.html', fun_fact = x)

@app.route('/home.html')
def home1():
	x     = random.choice(['I am from India','I like to work on Arduino','I like to travel'])
	return render_template('home.html', fun_fact = x)

@app.route('/projects.html')
def project():
	return render_template('projects.html')

@app.route('/piano.html')
def piano():
	return render_template('piano.html')


@app.route('/resume.html')
def resume():
	resume_data = db.getResumeData()
	return render_template('resume.html', resume_data = resume_data)


# @app.route('/processfeedback')
# def feedback():
# 	return render_template('processfeedback.html')

@app.route('/processfeedback.html', methods = ['POST'])
def processfeedback():
	feedback_data = request.form
	db.send_feedback(feedback_data)
	get_data = db.get_feedback()
	return render_template('processfeedback.html',feedback = get_data)
