from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime
import time
from bs4 import BeautifulSoup

def get_class_info(driver, department, semester):
    # Navigate to the page
    driver.get("https://soc.uvm.edu/")
    
    # Select the semester
    semester_select = driver.find_element(By.ID, "crit-srcdb")
    semester_select.click()
    
    if semester == "Spring 2025":
        spring_option = driver.find_element(By.CSS_SELECTOR, "option[value='202501']")
        spring_option.click()
    elif semester == "Fall 2025":
        fall_option = driver.find_element(By.CSS_SELECTOR, "option[value='202509']")
        fall_option.click()
    
    time.sleep(1)  # Wait for selection to take effect
    
    # Find and fill the keyword input
    keyword_input = driver.find_element(By.ID, "crit-keyword")
    keyword_input.clear()
    keyword_input.send_keys(department)
    keyword_input.send_keys(Keys.RETURN)
    
    # Wait for results to load
    wait = WebDriverWait(driver, 10)

    courses = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"[data-group^='code:{department}']")))

    return courses

def process_course(course, wait):
    course.click()
    # a quick sleep is necessary between each class as some courses were missing/duplicated
    # could probably be faster than .5 seconds but it's ok for now
    time.sleep(0.5)
    panel_content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".panel--kind-details.panel--visible .panel__content")))
    html_content = panel_content.get_attribute('innerHTML')
    return extract_course_data(html_content)


def extract_course_data(html_content):
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
    
    # Expanded Section Description
    expanded_section = soup.find('div', class_='section--expanded_sect_details')
    if expanded_section:
        expanded_content = expanded_section.find('div', class_='section__content')
        if expanded_content:
            # Extract section description
            section_desc_elem = expanded_content.find('div', class_='expanded-detail_learning-objectives')
            if section_desc_elem:
                # Remove the "Section Description: " prefix
                section_desc_text = section_desc_elem.text.replace('Section Description:', '').strip()
                course_data['section_description'] = section_desc_text
            
            # Extract section expectations
            expectations_elem = expanded_content.find('div', class_='expanded-detail_req-materials')
            if expectations_elem:
                # Remove the "Section Expectations: " prefix
                expectations_text = expectations_elem.text.replace('Section Expectations:', '').strip()
                course_data['section_expectations'] = expectations_text
            
            # Extract evaluation criteria
            evaluation_elem = expanded_content.find('div', class_='expanded-detail_technical-reqs')
            if evaluation_elem:
                # Remove the "Evaluation: " prefix
                evaluation_text = evaluation_elem.text.replace('Evaluation:', '').strip()
                course_data['evaluation'] = evaluation_text
    
    # SOC Comments
    soc_comments_section = soup.find('div', class_='section--clssnotes')
    if soc_comments_section:
        soc_content = soc_comments_section.find('div', class_='section__content')
        if soc_content:
            course_data['soc_comments'] = soc_content.text.strip()
    
    return course_data

def save_to_json(course_data, filename):
    """Save course data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(course_data, f, indent=2)
    print(f"Data saved to {filename}")

def scrape_semester(driver, department, semester):
    """Scrape courses for a specific semester"""
    print(f"\n=== Scraping {semester} courses ===")
    
    courses = get_class_info(driver, department, semester)
    all_courses = []
    
    for i, course in enumerate(courses):
        print(f"Processing {semester} course {i+1}/{len(courses)}")
        course_data = process_course(course, wait)
        if course_data:
            course_data['semester'] = semester
            all_courses.append(course_data)
    
    # Save semester-specific file
    if all_courses:
        filename = f"{department}_{semester.lower().replace(' ', '_')}_courses.json"
        save_to_json(all_courses, filename)
        print(f"Saved {len(all_courses)} courses to {filename}")
    
    return all_courses


if __name__ == "__main__":
    # Initialize the webdriver
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    department = "CS"
    
    # Scrape Fall courses
    fall_courses = scrape_semester(driver, department, "Fall 2025")
    
    # Scrape Spring courses
    spring_courses = scrape_semester(driver, department, "Spring 2025")
    
    # combined file
    all_courses = fall_courses + spring_courses
    if all_courses:
        combined_filename = f"{department}_all_courses.json"
        save_to_json(all_courses, combined_filename)
        print(f"\nCombined file created: {combined_filename}")
        print(f"Total courses: {len(all_courses)} ({len(fall_courses)} Fall + {len(spring_courses)} Spring)")
    
    driver.quit()