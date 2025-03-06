from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

driver = webdriver.Chrome()  # Run in headless mode
job = "frontend"
driver.get(f"https://www.naukri.com/{job}-jobs")
driver.implicitly_wait(10)

# Extract job titles, locations, and href links
naukri_name = driver.find_elements(By.CSS_SELECTOR, "a.title")
naukri_location = driver.find_elements(By.CSS_SELECTOR, "span.locWdth")

for name, location in zip(naukri_name[:5], naukri_location[:5]):  
    job_name = name.text
    job_location = location.text
    job_link = name.get_attribute("href")  # Extract the href attribute

    print("Job Name:", job_name)
    print("Location:", job_location)
    print("Job Link:", job_link)
    print("-" * 50)  # Separator for readability

# Close the browser
driver.quit()