import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LinkedinScraper:
    def __init__(self, company_name):
        self.driver = webdriver.Chrome('./chromedriver')
        self.company_name = company_name

    def login(self):
        self.driver.get('https://www.linkedin.com/')
        login_username = self.driver.find_element_by_id('login-email')
        login_password = self.driver.find_element_by_id('login-password')
        login_username.send_keys("rohanmahajan1993@gmail.com")
        login_password.send_keys("warriors93")
        login_submit = self.driver.find_element_by_id('login-submit')
        login_submit.click()

    def search(self):
        search_bar = self.driver.find_element_by_xpath(
            "//input[@role='combobox']")
        search_bar.send_keys(self.company_name)
        search_bar.send_keys(Keys.RETURN)

    def scrape(self):
        self.login()
        self.search()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        company_name = sys.argv[1]
    else:
        company_name = "Macys"
    linkedin_scraper = LinkedinScraper(company_name)
    linkedin_scraper.scrape()
