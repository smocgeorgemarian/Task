import requests as requests
from selenium import webdriver
from selenium.webdriver.common.by import By


class Scrapper:
    def __init__(self, url, api_url):
        self.URL = url
        self.api_URL = api_url
        self.driver = webdriver.Firefox()
        self.processed_data = dict()

    def parse_data(self) -> None:
        self.driver.get(self.URL)
        table_rows = self.driver.find_elements(By.XPATH, '/html/body/table/tbody/tr')[1:]
        for row in table_rows:
            self.process_family(row)
        self.driver.quit()

    def process_family(self, row) -> None:
        family = row.text.split("\n")[0]

        samples_url = f"{self.URL}{family}/Samples/"
        samples_driver = webdriver.Firefox()
        samples_driver.get(samples_url)
        hashes = map(lambda x: x.text.split('\n')[0],
                     samples_driver.find_elements(By.XPATH, '/html/body/table/tbody/tr')[1:])
        samples_driver.quit()
        self.processed_data[family] = hashes

    def pretty_print_data(self):
        print(self.processed_data)

    def add_data_to_database(self):
        for family in self.processed_data:
            for hash_value in self.processed_data[family]:
                requests.post(self.api_URL, json={"hash": hash_value, "family": family})
