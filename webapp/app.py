from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import re

app = Flask(__name__)
app.run(host='0.0.0.0')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def test_regex():
    data = request.json
    pattern = data['pattern']
    test_string = data['testString']
    matches = []
    try:
        regex = re.compile(pattern)
        matches = [match.group() for match in regex.finditer(test_string)]
    except re.error as e:
        return jsonify({'error': str(e), 'matches': []})

    return jsonify({'error': None, 'matches': matches})

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        return True
    else:
        return False
    
@app.route('/email', methods=['GET','POST'])
def email_validate():
    if request.method == 'POST':
        email = request.form['email']
        if validate_email(email):
            flash('Email is valid.', 'success')
        else:
            flash('Invalid email address.', 'error')
        return redirect(url_for('index'))
    return render_template('email.html')

@app.route('/notes')
def index():
    return render_template('notes.html')

@app.route('/feedback')
def index1():
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)