from selenium import  webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, traceback

gecko_binary = r'/usr/bin/geckodriver'
USERNAME = "linkedin_username"
PASSWORD = "linkedin_password"
CONTENT = "Hello world! This is message for Linkedin users"

try:
    driver = webdriver.Firefox(executable_path=gecko_binary)

    driver.get("https://www.linkedin.com/m/logout")
    time.sleep(1)

    driver.get("https://www.linkedin.com/")
    time.sleep(1)

    # input login
    elem = driver.find_element_by_id("login-email")
    elem.send_keys(USERNAME)

    # input password
    elem = driver.find_element_by_id("login-password")
    elem.send_keys(PASSWORD)
    elem.send_keys(Keys.ENTER)

    # wait for main page after login
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "nav-settings__dropdown-trigger"))
    )

    # show popup message window
    time.sleep(3)
    elem = driver.execute_script(" document.getElementsByClassName('share-box__open share-box__trigger')[0].click(); ")

    # input content
    js = "document.getElementsByClassName('mentions-texteditor__content')[0].innerHTML = \"{0}\"; ".format(CONTENT)
    driver.execute_script(js)

    # remove image preview (if exists)
    time.sleep(2)
    js = " if (document.getElementsByClassName('share-box__preview-close-btn').length>0) document.getElementsByClassName('share-box__preview-close-btn')[0].click(); "
    driver.execute_script(js)
    
    # accept
    js = " document.getElementsByClassName('share-actions__primary-action')[0].click(); "
    driver.execute_script(js)

    # accept (message visible for all)
    time.sleep(2)
    js = " document.getElementsByClassName('share-actions__primary-action')[0].click(); "
    driver.execute_script(js)

    print "Message sent!"

except Exception as e:
    traceback.print_exc()
finally:
    driver.quit

