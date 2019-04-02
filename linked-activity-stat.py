# -*- coding: utf-8 -*-

from selenium import  webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, traceback, re


gecko_binary = r'/usr/bin/geckodriver'
USERNAME = "***********"
PASSWORD = "*********"

PROFILE = 'https://www.linkedin.com/in/williamhgates/detail/recent-activity/shares/'


try:

    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/73.0.3683.68 Mobile/15E148 Safari/605.1")
    driver = webdriver.Firefox(profile, executable_path=gecko_binary)

    driver.get("https://www.linkedin.com/m/logout")
    time.sleep(1)

    driver.get("https://www.linkedin.com/uas/login?trk=uno-reg-guest-home-mobile-join")
    time.sleep(1)

    # input login
    elem = driver.find_element_by_id("username")
    elem.send_keys(USERNAME)

    # input password
    elem = driver.find_element_by_id("password")
    elem.send_keys(PASSWORD)
    elem.send_keys(Keys.ENTER)

    # wait for main page after login
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "nav-item__icon"))
    )

    driver.get(PROFILE)
    time.sleep(3)

    items = driver.find_elements_by_class_name('feed-shared-update-v2__scroll')
    if items:
        print("Total items: {}".format(len(items)))
    for item in items:
        author = item.find_element_by_tag_name('h3').get_attribute('innerText')
        author = author.split('\n')[0]
        
        try:
            message = item.find_element_by_class_name('feed-shared-update-v2__commentary').text
            message = "{}...".format( message.replace(r'\nhasztag\n', ' ').encode('utf-8')[0:55] )
        except Exception as e:
            message = ""

        try:
            el = item.find_element_by_class_name('feed-shared-social-counts__num-likes').find_element_by_tag_name('span').text
            shares = re.sub(r'\D', '', el )
        except Exception as e:
            shares = -1

        try:
            el = item.find_element_by_class_name('feed-shared-social-counts__num-comments').find_element_by_tag_name('span').text
            comments = re.sub(r'\D', '', el )
        except Exception as e:
            comments = -1

        try:
            el = item.find_element_by_class_name('content-analytics-entry-point').find_element_by_tag_name('span').text
            views = re.sub(r'\D', '', el )
        except Exception as e:
            views = -1
        
        try:
            el = item.find_element_by_class_name('feed-shared-social-action-bar__comment-link')
            link = el.get_attribute('href')
            link = link.split('?')[0]
        except Exception as e:
            link = ""

        print("="*40)
        print("URL: {}".format(link))
        print("Autor: {}".format(author.decode('unicode-escape')))
        print("Tekst: {}".format(message))
        if shares>0:
            print("Polecenia: {}".format(shares))
        if comments>0:
            print("Komentarze: {}".format(comments))
        if views>0:
            print("Wyświetleń: {}".format(views))


except Exception as e:
    traceback.print_exc()
finally:
    driver.quit

