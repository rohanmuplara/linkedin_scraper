import datetime
import sys
import time
import logging as custom_logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LinkedinScraper:
    def __init__(self, company_name):
        self.driver = webdriver.Chrome('./chromedriver')
        self.company_name = company_name
        current_time = datetime.datetime.utcnow().strftime(
            "%I:%M%p on %B %d, %Y")
        log_file_name = company_name + " " + current_time
        custom_logging.basicConfig(
            level=custom_logging.INFO,
            filename=log_file_name,
            filemode='w',
            format='%(levelname)s - %(message)s')

    def login(self):
        self.driver.get('https://www.linkedin.com/')
        login_username = self.driver.find_element_by_id('login-email')
        login_password = self.driver.find_element_by_id('login-password')
        login_username.send_keys("rohanmahajan1993@gmail.com")
        login_password.send_keys("warriors93")
        login_submit = self.driver.find_element_by_id('login-submit')
        login_submit.click()

    def generate_connection_urls(self):
        search_bar = self.driver.find_element_by_xpath(
            "//input[@role='combobox']")
        search_bar.send_keys(self.company_name)
        search_bar.send_keys(Keys.RETURN)
        connections = set()
        while True:
            time.sleep(10)
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight / 2.0)")
            time.sleep(5)
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)")
            search_results = self.driver.find_elements_by_xpath(
                "//a[@data-control-name='search_srp_result']")
            for search_result in search_results:
                connection_url = search_result.get_attribute("href")
                connections.add(connection_url)
            try:
                next_button = self.driver.find_element_by_xpath(
                    "//button[contains(@class, 'artdeco-pagination__button--next')]"
                )
                next_button.click()
                break
            except:
                break
        print connections
        return connections

    def add_connections(self, connection_urls):
        for connection_url in connection_urls:
            self.driver.get(connection_url)
            try:
                connect_button = self.driver.find_element_by_xpath(
                    "//button[contains(@class, 'pv-s-profile-actions--connect')]"
                )
                connect_button.click()
                import pdb
                pdb.set_trace()
            except:
                try:
                    overflow_button = self.driver.find_element_by_xpath(
                        "//button[contains(@class, 'pv-s-profile-actions__overflow-toggle')]"
                    )
                    connect_button = self.driver.find_element_by_xpath(
                        "//button[contains(@class, 'pv-s-profile-actions--connect')]"
                    )
                    connect_button.click()
                except:
                    a = 5

    def scrape(self):
        self.login()
        connection_urls = self.generate_connection_urls()
        self.add_connections(connection_urls)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        company_name = sys.argv[1]
    else:
        company_name = "Macys"
    linkedin_scraper = LinkedinScraper(company_name)
    linkedin_scraper.scrape()
