import time
from selenium import webdriver


class LinkedinScraper:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')

    def login(self):
        self.driver.get('https://www.linkedin.com/')
	login_username = self.driver.find_element_by_id('login-email')
	login_password = self.driver.find_element_by_id('login-password')
        login_username.send_keys("rohanmahajan1993@gmail.com")
        login_password.send_keys("warriors93")
	login_submit = self.driver.find_element_by_id('login-submit')
        login_submit.click()

    def scrape(self):
        self.login()


if __name__ == "__main__":
    linkedin_scraper = LinkedinScraper()
    linkedin_scraper.scrape()
