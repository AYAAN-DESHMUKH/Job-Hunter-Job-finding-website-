from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from PyPDF2 import PdfReader
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import unquote
from resume_builder.routes import resume_bp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'kalsekarkipublic'

app.register_blueprint(resume_bp)
# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Global variable to store scraping status and results
scraping_status = {
    "status": "idle", 
    "job_data": [],
    "progress": 0,
    "total_tasks": 0,
    "completed_tasks": 0
}

@app.before_request
def initialize_bookmarks():
    if 'bookmarks' not in session:
        session['bookmarks'] = []

@app.route('/bookmark/<job_id>', methods=['POST'])
def bookmark_job(job_id):
    decoded_job_id = unquote(job_id)
    if decoded_job_id not in session['bookmarks']:
        session['bookmarks'].append(decoded_job_id)
        session.modified = True
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/bookmarks')
def bookmarks():
    bookmarked_jobs = [job for job in scraping_status["job_data"] if job["name"] in session['bookmarks']]
    return render_template('bookmarks.html', bookmarked_jobs=bookmarked_jobs)

@app.route('/clear_bookmarks', methods=['POST'])
def clear_bookmarks():
    session['bookmarks'] = []
    session.modified = True
    return jsonify({"success": True})

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/Jobseekers')
def Jobseekers():
    return render_template('Jobseekers.html')

@app.route('/Blog')
def Blog():
    return render_template('Blog.html')

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
        
        reader = PdfReader(filepath)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        
        keywords = ['c++', 'frontend developer', 'backend developer', 'python', 'java', 'javascript', 'react', 'angular', 'node.js', 'sql', 'devops', 'cloud', 'aws', 'azure', 'docker', 'kubernetes']
        found_keywords = [keyword for keyword in keywords if keyword.lower() in text.lower()]
        
        global scraping_status
        scraping_status = {
            "status": "in progress", 
            "job_data": [],
            "progress": 0,
            "total_tasks": len(found_keywords) * 3,  # 3 sites per keyword
            "completed_tasks": 0
        }
        
        threading.Thread(target=scrape_jobs, args=(found_keywords,)).start()
        return render_template('loading.html')
    
    return redirect(request.url)

@app.route('/scraping_status')
def get_scraping_status():
    global scraping_status
    # Calculate progress percentage
    if scraping_status["total_tasks"] > 0:
        scraping_status["progress"] = int((scraping_status["completed_tasks"] / scraping_status["total_tasks"]) * 100)
    return jsonify(scraping_status)

@app.route('/jobs')
def show_jobs():
    global scraping_status
    if scraping_status["status"] == "complete":
        return render_template('jobs.html', job_data=scraping_status["job_data"])
    else:
        return redirect(url_for('home'))
#hvhfmhf
def scrape_naukri(keyword):
    options = Options()
    options.add_argument("--headless")
    service = Service()
    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        driver.get(f"https://www.naukri.com/{keyword}-jobs")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.title"))
        )

        naukri_name = driver.find_elements(By.CSS_SELECTOR, "a.title")
        naukri_location = driver.find_elements(By.CSS_SELECTOR, "span.locWdth")
        
        jobs = []
        for name, location in zip(naukri_name[:5], naukri_location[:5]):  
            jobs.append({
                "name": name.text, 
                "location": location.text, 
                "link": name.get_attribute("href"),
                "source": "Naukri"
            })
        
        return jobs
    except Exception as e:
        print(f"Error scraping Naukri: {e}")
        return []
    finally:
        driver.quit()
        update_progress()

def scrape_fresherworld(keyword):
    options = Options()
    options.add_argument("--headless")
    service = Service()
    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        driver.get(f"https://www.freshersworld.com/jobs/jobsearch/{keyword}-jobs")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.col-md-12.col-lg-12.col-xs-12.padding-none.job-container.jobs-on-hover.top_space"))
        )

        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.col-md-12.col-lg-12.col-xs-12.padding-none.job-container.jobs-on-hover.top_space")
        
        jobs = []
        for card in job_cards[:5]:
            try:
                job_name = card.find_element(By.CSS_SELECTOR, "span.wrap-title.seo_title").text
                job_location = card.find_element(By.CSS_SELECTOR, "a.bold_font").text
                job_link = card.get_attribute("job_display_url")
                jobs.append({
                    "name": job_name, 
                    "location": job_location, 
                    "link": job_link,
                    "source": "Freshersworld"
                })
            except Exception as e:
                print(f"Error extracting job details from Freshersworld: {e}")
        
        return jobs
    except Exception as e:
        print(f"Error in scrape_fresherworld for keyword '{keyword}': {e}")
        return []
    finally:
        driver.quit()
        update_progress()

def scrape_jobsora(keyword):
    options = Options()
    options.add_argument("--headless")
    service = Service()
    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        driver.get(f"https://in.jobsora.com/jobs?query={keyword}")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.u-text-double-line"))
        )

        jobsora_name = driver.find_elements(By.CSS_SELECTOR, "a.u-text-double-line")
        jobsora_location = driver.find_elements(By.CSS_SELECTOR, "div.c-job-item__info-item")
        
        jobs = []
        for name, location in zip(jobsora_name[:5], jobsora_location[:5]):  
            jobs.append({
                "name": name.text, 
                "location": location.text, 
                "link": name.get_attribute("href"),
                "source": "Jobsora"
            })
        
        return jobs
    except Exception as e:
        print(f"Error scraping Jobsora: {e}")
        return []
    finally:
        driver.quit()
        update_progress()

def update_progress():
    global scraping_status
    scraping_status["completed_tasks"] += 1
    if scraping_status["total_tasks"] > 0:
        scraping_status["progress"] = int((scraping_status["completed_tasks"] / scraping_status["total_tasks"]) * 100)

def scrape_jobs(keywords):
    global scraping_status
    job_data = []
    
    with ThreadPoolExecutor() as executor:
        futures = []
        for keyword in keywords:
            futures.append(executor.submit(scrape_naukri, keyword))
            futures.append(executor.submit(scrape_jobsora, keyword))
            futures.append(executor.submit(scrape_fresherworld, keyword))
        
        for future in as_completed(futures):
            try:
                jobs = future.result()
                if jobs:
                    job_data.extend(jobs)
                    scraping_status["job_data"] = job_data
            except Exception as e:
                print(f"Error in scraping task: {e}")
    
    scraping_status["status"] = "complete"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)