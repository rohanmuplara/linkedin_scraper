import time
from selenium import webdriver


class LinkedinScraper:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')

    def login(self):
        self.driver.get('https://www.linkedin.com/feed/')

    def scrape(self):
        self.login()


if __name__ == "__main__":
    linkedin_scraper = LinkedinScraper()
    linkedin_scraper.scrape()
