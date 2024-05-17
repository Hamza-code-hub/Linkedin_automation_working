from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
import os

def login(driver, username, password):
    try:
        driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        user.send_keys(username)
        password_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
        password_elem.send_keys(password)
        password_elem.send_keys(Keys.RETURN)
        print("Login successful.")
    except TimeoutException:
        print("Timeout while trying to log in.")
    except Exception as e:
        print(f"An error occurred during login: {e}")

def connect_with_profile(driver, profile_url, message=None):
    try:
        driver.get(profile_url)

        # Try finding the Connect button with various locators
        try:
            connect_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button/span"))
            )
        except TimeoutException:
            connect_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'pvs-profile-actions__action')]"))
            )

        connect_button.click()

        # Wait for the Connect dialog to appear
        connect_dialog = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
        )

        # If a message is provided, click Add a note and send the message
        if message:
            add_note_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[1]/span"))
            )
            add_note_button.click()

            message_box = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/div[1]/textarea"))
            )
            message_box.send_keys(message)

        # Click the "Send now" button to send the connection request
        send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[4]/button[2]/span"))
        )
        send_button.click()

        print("Connection request sent successfully.")
    except TimeoutException as te:
        print(f"Timeout while trying to send connection request: {te}")
    except NoSuchElementException as nse:
        print(f"Connect button or dialog not found: {nse}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')

    service = Service("C:\\Program Files (x86)\\Chrome Driver\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)

    your_username = os.getenv("LINKEDIN_USERNAME", "ua1552284@gmail.com")
    your_password = os.getenv("LINKEDIN_PASSWORD", "aliusman123")

    print(f"Username: {your_username}")
    print(f"Password: {your_password}")

    if not your_username or not your_password:
        print("Username or password not set.")
    else:
        login(driver, your_username, your_password)

        profile_url = "https://www.linkedin.com/in/sumaira-ilyas-50b3a6246/" 
        message = "Hi, I'm interested in connecting with you on LinkedIn."
#if you want send request with massage then use these massage veriable 
        connect_with_profile(driver, profile_url, message)
#other wise use
        #connect_with_profile(driver, profile_url)
    driver.quit()
