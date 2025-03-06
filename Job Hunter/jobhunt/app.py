from flask import Flask, render_template, request, redirect, url_for, jsonify
from PyPDF2 import PdfReader
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import threading

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Global variable to store scraping status and results
scraping_status = {"status": "idle", "job_data": []}

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
        
        # Start scraping in the background
        global scraping_status
        scraping_status = {"status": "in progress", "job_data": []}
        threading.Thread(target=scrape_jobs, args=(found_keywords,)).start()
        
        # Render the loading screen
        return render_template('loading.html')
    
    return redirect(request.url)

@app.route('/scraping_status')
def get_scraping_status():
    global scraping_status
    return jsonify(scraping_status)

@app.route('/jobs')
def show_jobs():
    global scraping_status
    if scraping_status["status"] == "complete":
        return render_template('jobs.html', job_data=scraping_status["job_data"])
    else:
        return redirect(url_for('home'))

def scrape_jobs(keywords):
    global scraping_status
    job_data = []
    
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    service = Service()  # Use the default GeckoDriver service
    driver = webdriver.Firefox(service=service, options=options)
    
    for keyword in keywords:
        driver.get(f"https://www.naukri.com/{keyword}-jobs")
        driver.implicitly_wait(10)

        naukri_name = driver.find_elements(By.CSS_SELECTOR, "a.title")
        naukri_location = driver.find_elements(By.CSS_SELECTOR, "span.locWdth")
        
        for name, location in zip(naukri_name[:5], naukri_location[:5]):  
            job_link = name.get_attribute("href")  # Extract the href attribute
            job_data.append({
                "name": name.text, 
                "location": location.text, 
                "link": job_link  # Add the job link to the dictionary
            })
    
    driver.quit()
    
    # Update scraping status
    scraping_status = {"status": "complete", "job_data": job_data}

if __name__ == '__main__':
    app.run(debug=True)