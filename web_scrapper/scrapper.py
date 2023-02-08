import re

import requests as requests


class Scrapper:
    def __init__(self, url, api_url):
        self.url = url
        self.api_url = api_url

    def parse_data(self) -> None:
        session_obj = requests.Session()

        response = session_obj.get(self.url)
        content = response.text
        table_start = content.index('id="list"')
        data = re.findall(r"<tr>.*</tr>", content[table_start:])
        for tag in data[2:]:
            family_match = re.search(r"<a.*>(.*)</a>", tag)
            family = family_match[family_match.lastindex]
            self.process_family(family)

    def process_family(self, family: str) -> None:
        pass

        samples_url = f"{self.url}{family}/Samples/"

        session_obj = requests.Session()
        response = session_obj.get(samples_url)
        if response.status_code == 404:
            samples_url = f"{self.url}{family}/"
            session_obj = requests.Session()
            response = session_obj.get(samples_url)

        if response.status_code == 404:
            raise Exception("Something went wrong")

        content = response.text
        table_start = content.index('id="list"')
        data = re.findall(r"<tr>.*</tr>", content[table_start:])
        hashes = list()
        for tag in data[2:]:
            sample_match = re.search(r"<a.*>(.*)</a>", tag)
            sample = sample_match[sample_match.lastindex].split(".")[0]
            requests.post(self.api_url, json={"hash": sample, "family": family})

