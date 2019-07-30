
import sys, time, random, traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class IgPhotosLikeBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def delayForBrowser(self, delay=3000):
        time.sleep(delay/1000.00)

    def destroyBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        self.delayForBrowser()
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        self.delayForBrowser()
        user_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_elem.clear()
        user_elem.send_keys(self.username)
        pass_elem = driver.find_element_by_xpath("//input[@name='password']")
        pass_elem.clear()
        pass_elem.send_keys(self.password)
        pass_elem.send_keys(Keys.RETURN)
        self.delayForBrowser()

    def likePhoto(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        self.delayForBrowser()

        img_hrefs = []
        for i in range(1, 10):
            try:
                self.delayForBrowser(random.randint(2, 4))
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view if '.com/p/' in elem.get_attribute('href')]
                [img_hrefs.append(href) for href in hrefs_in_view if href not in img_hrefs]
            except Exception:
                continue

        # like photo operation
        for img_href in img_hrefs:
            try:
                delay = random.randint(250, 1500)
                print("Like goes to {0} - {1}".format(img_href, delay))
                driver.get(img_href)
                self.delayForBrowser(delay)
                def like_button(): return driver.find_element_by_xpath('//span[@aria-label="Lubię to!"]').click()
                like_button().click()
            except Exception as e:
                # print(str(e))
                pass


if __name__ == "__main__":

    username = "IG_USERNAME"
    password = "IG_PASSWORD"

    hashtags = """
    #polskadziewczyna #polishgirl #poland #girl #instagirl #polska #instagood #love 
    #photooftheday #me #selfie #makeup #followme #fashion #photography #l4l 
    #polishboy #happy #smile #warszawa #brunette #polskakobieta #polishwoman 
    #instaphoto #photo #beauty #blonde #beautiful #warsaw #picoftheday
    """

    try:
        ig = IgPhotosLikeBot(username, password)
        ig.login()

        while True:
            tag = ""
            while not tag:
                # find random non empty tag
                tag = random.choice(hashtags.split("#")).strip()
            print("And the hashtag is '{}'".format(tag))

            ig.likePhoto(tag)
    except Exception as e:
        print(str(e))
    finally:
        ig.destroyBrowser()
