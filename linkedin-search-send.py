# -*- coding: utf-8 -*-

# (c) 2019 Marian Witkowski

from selenium import  webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, traceback

gecko_binary = r'/usr/bin/geckodriver'
USERNAME = "**************"
PASSWORD = "**************"

KEYWORDS = u"programista .NET Warszawa"
SUBJECT = u"Wiadomość testowa"
CONTENT = u"Cześć {}, zapraszam do kontaktu ...."

try:
    driver = webdriver.Chrome()

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

    js = " document.getElementsByClassName('artdeco-dismiss')[0].click(); "
    driver.execute_script(js)

    elem = driver.find_element_by_xpath("/html/body/header/div/form/div/div/div/artdeco-typeahead-deprecated/artdeco-typeahead-deprecated-input/input")
    elem.send_keys(KEYWORDS)
    elem.send_keys(Keys.ENTER)

    time.sleep(10)

    elem = driver.find_element_by_class_name("search-results__see-all-cards")
    elem.click()
    time.sleep(2)

    persons = []
    offset = 0
    items = driver.find_elements_by_class_name('search-result__occluded-item')
    for item in items:
        try:
            offset += 200
            personLink = item.find_element_by_class_name('search-result__result-link').get_attribute('href')
            personName = item.find_element_by_class_name('actor-name').text
            persons.append( (personName, personLink)  )
            driver.execute_script("window.scrollTo(0, {});".format(offset))
            time.sleep(1)
        except Exception as e:
            pass
    
    print(persons)

    for person in persons:
        (name, link) = person
        driver.get(link)
        time.sleep(2)

        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "nav-settings__dropdown-trigger"))
        )

        btnMsg = driver.find_element_by_class_name('pv-s-profile-actions--send-in-mail')
        btnMsg.click()

        subject = driver.find_element_by_class_name('msg-form__subject')
        subject.send_keys(SUBJECT)

        message = driver.find_element_by_class_name('msg-form__contenteditable')
        message.send_keys(CONTENT.format(name))

        #btnSend = driver.find_element_by_class_name('msg-form__send-button')
        #btnSend.click()

        print "Message to {} sent!".format(name.encode('utf-8'))

except Exception as e:
    traceback.print_exc()
finally:
    driver.quit

