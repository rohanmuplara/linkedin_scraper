import datetime
import logging
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LinkedinScraper:
    def __init__(self, company_name, search_term, message_term):
        self.driver = webdriver.Chrome('./chromedriver')
        self.company_name = company_name
        self.search_term = search_term
        current_time = datetime.datetime.utcnow().strftime(
            "%I:%M%p on %B %d, %Y")
        log_file_name = company_name + " " + current_time + ".log"
        logging.basicConfig(
            level=logging.INFO,
            filename=log_file_name,
            filemode='w',
            format='%(levelname)s - %(message)s')
        with open('message.txt', 'r') as message_file:
            self.message = message_file.read().replace('\n', '').replace(
                "INSERT_HERE", message_term)
        logging.info("message to be sent is" + self.message)

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
        search_bar.send_keys(self.search_term)
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
            except:
                break
        print connections
        return connections

    def handle_connect_button(self):
        connect_button = self.driver.find_element_by_xpath(
            "//button[contains(@class, 'pv-s-profile-actions--connect')]")
        connect_button.click()
        add_note_button = self.driver.find_element_by_xpath(
            "//button[contains(@class, 'button-secondary-large mr1')]")
        add_note_button.click()
        message_box = self.driver.find_element_by_id("custom-message")
        message_box.send_keys(self.message)
        send_invitation_button = self.driver.find_element_by_xpath(
            "//button[contains(@class, 'button-primary-large ml1')]")
        send_invitation_button.click()

    def add_connections(self, connection_urls):
        for connection_url in connection_urls:
            self.driver.get(connection_url)
            import pdb
            pdb.set_trace()
            current_job = self.driver.find_element_by_xpath(
                "//h2[contains(@class, 'pv-top-card-section__headline mt1 t-18 t-black t-normal')]"
            ).text
            if self.company_name not in current_job:
                logging.error("This person has changed jobs" + connection_url)
                continue
            try:
                self.handle_connect_button()
                logging.info("we have successfully connected with" +
                             connection_url)
            except:
                try:
                    overflow_button = self.driver.find_element_by_xpath(
                        "//button[contains(@class, 'pv-s-profile-actions__overflow-toggle')]"
                    )
                    overflow_button.click()
                    self.handle_connect_button()
                    logging.info("we have successfully connected with" +
                                 connection_url)
                except:
                    logging.error(
                        "We are not able to connect with this connection_url" +
                        connection_url)

    def scrape(self):
        self.login()
        connection_urls = self.generate_connection_urls()
        self.add_connections(connection_urls)


if __name__ == "__main__":
    company_name = raw_input("Please enter the company name")
    search_term = raw_input("Please enter what should be searched")
    message_term = raw_input(
        "Please enter what should be used to be replaced in message")
    linkedin_scraper = LinkedinScraper(company_name, search_term, message_term)
    linkedin_scraper.scrape()
