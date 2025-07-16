from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime
import time

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

    course_codes = []

    for course in courses:
        course.click()
        print(course.get_attribute('innerHTML'))
        try:
            # gets course codes (this takes from the "search results" panel. only courses at the start of a "course" have "result__code", ex: 1210 B-E, only B is appended)
            # i need to access the text in the right panel instead. not sure how to get there
            course_codes.append(course.find_element(By.CLASS_NAME, "result__code").text)
        except:
            print("No code found")

    print(course_codes)
    print(len(course_codes))
        
    driver.quit()

if __name__ == "__main__":
    get_class_info()