from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime
import time

def get_cs_class_names():
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



    print(courses[0].click())
    time.sleep(5)



    # # Extract class codes
    # class_codes = [course.get_attribute("data-group")[-7:] for course in courses]
    
    # # Save the data
    # course_data = {
    #     'class_codes': class_codes,
    #     'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     'total_classes': len(class_codes)
    # }
    
    # output_file = f"cs_class_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     json.dump(course_data, f, indent=2)
        
    # print(f"Successfully scraped {len(class_codes)} CS class codes")
    # print("First few classes:")
    # for code in class_codes[:5]:
    #     print(f"- {code}")
    
        
    driver.quit()

if __name__ == "__main__":
    get_cs_class_names()