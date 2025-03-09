from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resume Builder, Summarizer & Job Finder</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
            }
            .container {
                max-width: 900px;
                width: 90%;
                text-align: center;
                margin-top: 20px;
            }
            .header {
                font-size: 1.32em;
                font-weight: bold;
                padding: 20px;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.2);
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(10px);
            }
            .card {
                background: rgba(255, 255, 255, 0.2);
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(10px);
                border-radius: 12px;
                padding: 20px;
                margin: 15px 0;
                text-align: left;
            }
            .btn {
                display: block;
                width: 200px;
                padding: 10px;
                margin: 20px auto;
                background: #ff7eb3;
                color: white;
                font-size: 1.1em;
                text-align: center;
                text-decoration: none;
                border-radius: 8px;
                transition: 0.3s;
            }
            .btn:hover {
                background: #ff5277;
            }
            h1, h2, h3 {
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
            }
            p {
                font-size: 1.1em;
                line-height: 1.6;
            }
            ul {
                padding-left: 20px;
                list-style-type: none;
            }
            li {
                margin-bottom: 8px;
            }
            a.mail-link {
                color: #ffdb70;
                text-decoration: none;
                font-weight: bold;
            }
            a.mail-link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Resume Builder, Summarizer & Job Finder</h1>
            </div>
            
            <div class="card">
                <h2>What We Do</h2>
                <p>Our platform helps you analyze your resume, generate a summary, and find job opportunities tailored to your skills.</p>
            

            <div class="card">
                <h2>Key Features</h2>
                <ul>
                    <li>🔍 AI-powered resume analysis</li>
                    <li>📄 Summarizes your key skills and experience</li>
                    <li>💼 Provides job recommendations based on your resume</li>
                    <li>⚡ Fast and accurate results</li>
                </ul>
            </div>

            <div class="card">
                <h2>How It Works</h2>
                <p>Simply upload your resume (PDF or text format), and our AI-driven system will generate a concise summary of your experience while suggesting job roles that match your profile.</p>
            </div>

            <div class="card">
                <h2>Coming Soon</h2>
                <p>🔹 LinkedIn integration for better job matches <br> 
                   🔹 Wide range of job availability all over the country <br> 
                   🔹 Resume optimization tips</p>
            </div>
            </div>

            <a href="/about" class="btn">Learn More</a>
        </div>
    </body>
    </html>
    """

@app.route("/about")
def about():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About Us</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
            }
            .container {
                max-width: 800px;
                width: 90%;
                text-align: center;
                margin-top: 20px;
                padding: 20px;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.2);
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(10px);
            }
            .btn {
                display: block;
                width: 200px;
                padding: 10px;
                margin: 20px auto;
                background: #ff7eb3;
                color: white;
                font-size: 1.1em;
                text-align: center;
                text-decoration: none;
                border-radius: 8px;
                transition: 0.3s;
            }
            .btn:hover {
                background: #ff5277;
            }
            a.mail-link {
                color: #ffdb70;
                text-decoration: none;
                font-weight: bold;
            }
            a.mail-link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>About Us</h1>
            <p>Welcome to Resume Builder, Summarizer & Job Finder! Our platform is designed to help job seekers enhance their resumes, summarize key qualifications, and discover job opportunities with ease.</p>
            <p>Our AI-driven system ensures that your resume gets the attention it deserves by highlighting your strengths and matching you with relevant job openings.</p>
            <p>Stay tuned for upcoming features that will further enhance your job-seeking experience!</p>
            <h2>Key Contributors:</h2>
                <ul>
                    <li><a href="https://mail.google.com/mail/?view=cm&fs=1&to=24dco01@aiktc.ac.in" target="_blank" class="mail-link">📧  24dco01@aiktc.ac.in</a></li>
                    <li><a href="https://mail.google.com/mail/?view=cm&fs=1&to=24dco02@aiktc.ac.in" target="_blank" class="mail-link">📧  24dco02@aiktc.ac.in</a></li>
                    <li><a href="https://mail.google.com/mail/?view=cm&fs=1&to=24dco03@aiktc.ac.in" target="_blank" class="mail-link">📧  24dco03@aiktc.ac.in</a></li>
                    <li><a href="https://mail.google.com/mail/?view=cm&fs=1&to=24dco05@aiktc.ac.in" target="_blank" class="mail-link">📧  24dco05@aiktc.ac.in</a></li>
                </ul>
            <a href="/" class="btn">Back to Home</a>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
