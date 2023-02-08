from selenium import webdriver
from selenium.webdriver.common.by import By



class Scrapper:
    def __init__(self, URL):
        self.URL = URL
        self.driver = webdriver.Firefox()

    def parse_data(self):
        self.driver.get(self.URL)
        table = self.driver.find_element(By.XPATH, '/html/body/table/tbody')

        print(table)
        self.driver.quit()

