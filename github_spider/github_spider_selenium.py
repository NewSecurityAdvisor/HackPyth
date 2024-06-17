from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def scrape_repo(url):
    driver = webdriver.Chrome()  # Replace with your preferred browser driver
    driver.get(url)

    # Check if "Show Code" button exists before waiting
    if driver.find_element(By.CSS_SELECTOR, ".show-code-button").is_displayed():
        show_code_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".show-code-button"))
        )
        show_code_button.click()
    driver.quit()

# Example usage
url = "https://github.com/NewSecurityAdvisor/HackPyth"  # Replace with a public repository URL
scrape_repo(url)
