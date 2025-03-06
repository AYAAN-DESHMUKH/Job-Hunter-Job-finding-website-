from flask import Flask, render_template, request, redirect, url_for
from PyPDF2 import PdfReader
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def home():
    categories = [
        {"name": "Construction", "icon_class": "fas fa-briefcase", "open_positions": 45},
        {"name": "Information Technology", "icon_class": "fas fa-laptop-code", "open_positions": 78},
        {"name": "Healthcare", "icon_class": "fas fa-stethoscope", "open_positions": 62},
        {"name": "Education", "icon_class": "fas fa-chalkboard-teacher", "open_positions": 35},
        {"name": "Non-Profit", "icon_class": "fas fa-hands-helping", "open_positions": 22},
        {"name": "Finance", "icon_class": "fas fa-chart-line", "open_positions": 50},
        {"name": "Engineering", "icon_class": "fas fa-tools", "open_positions": 40},
        {"name": "Management", "icon_class": "fas fa-user-tie", "open_positions": 30},
    ]
    return render_template('index.html', categories=categories)

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return redirect(request.url)
    
    file = request.files['resume']
    if file.filename == '':
        return redirect(request.url)
    
    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Extract text from PDF using PdfReader
        reader = PdfReader(filepath)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        
        # Extract keywords (this is a simple example, you can use more advanced NLP techniques)
        keywords = ['c++', 'frontend developer', 'backend developer', 'python', 'java', 'javascript', 'react', 'angular', 'node.js', 'sql', 'devops', 'cloud', 'aws', 'azure', 'docker', 'kubernetes']
        found_keywords = [keyword for keyword in keywords if keyword.lower() in text.lower()]
        
        return render_template('jobs.html', keywords=found_keywords)
    
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)