from selenium import webdriver
from selenium.webdriver.common.by import By


class Scrapper:
    def __init__(self, URL):
        self.URL = URL
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

        samples_URL = f"{self.URL}{family}/Samples/"
        samples_driver = webdriver.Firefox()
        samples_driver.get(samples_URL)
        hashes = map(lambda x: x.text.split('\n')[0],
                         samples_driver.find_elements(By.XPATH, '/html/body/table/tbody/tr')[1:])
        samples_driver.quit()
        self.processed_data[family] = hashes
        a = 1

    def pretty_print_data(self):
        print(self.processed_data)