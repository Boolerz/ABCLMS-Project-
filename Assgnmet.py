#This code assumes you have the following templates in a folder named templates:

#1. index.html for displaying assignments and a form to post new assignments.
#2. post_assignment.html for the form to post new assignments.
#3. submit_answer.html for the form to submit answers.
#Make sure you also have a folder named uploads where uploaded PDF files will be stored.

#This is just a basic example to get you started. You may need to add more features 
#like authentication, error handling, and file management according to your requirements.
from flask import Flask, render_template, request, redirect, url_for, send_file
import os

app = Flask(__name__)

# Store assignments and answers in a dictionary
assignments = {}
answers = {}

@app.route('/')
def index():
    return render_template('index.html', assignments=assignments)

@app.route('/post_assignment', methods=['GET', 'POST'])
def post_assignment():
    if request.method == 'POST':
        assignment_title = request.form['title']
        assignment_description = request.form['description']
        assignments[assignment_title] = assignment_description
        return redirect(url_for('index'))
    return render_template('post_assignment.html')

@app.route('/submit_answer/<assignment_title>', methods=['GET', 'POST'])
def submit_answer(assignment_title):
    if request.method == 'POST':
        answer_text = request.form['answer']
        answers[assignment_title] = answer_text

        # Save PDF if uploaded
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                answers[assignment_title] = filename

        return redirect(url_for('index'))
    return render_template('submit_answer.html', assignment_title=assignment_title)

@app.route('/download_answer/<assignment_title>')
def download_answer(assignment_title):
    answer_file = answers.get(assignment_title)
    if answer_file:
        return send_file(answer_file, as_attachment=True)
    else:
        return "No answer submitted yet for this assignment."

if __name__ == '__main__':
    app.run(debug=True)
