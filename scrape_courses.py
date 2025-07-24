from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime
import time
from bs4 import BeautifulSoup

def get_class_info():
    # Initialize the webdriver
    driver = webdriver.Chrome()
    
    # Navigate to the page
    driver.get("https://soc.uvm.edu/")
    
    # Find and fill the keyword input
    keyword_input = driver.find_element(By.ID, "crit-keyword")
    keyword_input.clear()
    keyword_input.send_keys("CS")
    keyword_input.send_keys(Keys.RETURN)
    
    # Wait for results to load
    wait = WebDriverWait(driver, 10)

    courses = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-group^='code:CS']")))

    courses[0].click()

    # <div class="panel panel--2x panel--kind-details panel--visible" data-panel-id="2" style="left: 700px;">
    panel_content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".panel--kind-details.panel--visible .panel__content")))
    html_content = panel_content.get_attribute('innerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract course information
    course_data = {}
    
    # Course code and section
    course_code_elem = soup.find('div', class_='dtl-course-code')
    if course_code_elem:
        course_data['course_code'] = course_code_elem.text.strip()
    
    section_elem = soup.find('div', class_='dtl-section')
    if section_elem:
        course_data['section'] = section_elem.text.strip()
    
    # Course title
    title_elem = soup.find('div', class_='detail-title')
    if title_elem:
        course_data['title'] = title_elem.text.strip()
    
    # Credit hours
    hours_elem = soup.find('div', class_='detail-hours_html')
    if hours_elem:
        course_data['credit_hours'] = hours_elem.text.replace('Credit Hours:', '').strip()
    
    # Meeting info
    meeting_elem = soup.find('div', class_='meet')
    if meeting_elem:
        course_data['meeting_info'] = meeting_elem.text.strip()
    
    # Instructor
    instructor_elem = soup.find('div', class_='instructor-detail')
    if instructor_elem:
        course_data['instructor'] = instructor_elem.text.strip()
    
    # Description
    description_elem = soup.find('div', class_='section--description')
    if description_elem:
        desc_content = description_elem.find('div', class_='section__content')
        if desc_content:
            course_data['description'] = desc_content.text.strip()
    
    # save
    with open('course_data.json', 'w') as f:
        json.dump(course_data, f, indent=2)
    
    print("Data saved to course_data.json")
        
    driver.quit()

if __name__ == "__main__":
    get_class_info()


# notes
# send to json