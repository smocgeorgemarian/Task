import re

import requests as requests

LINK = r"<a.*>(.*)</a>"

TABLE_ROW = r"<tr>.*</tr>"


class Scrapper:
    def __init__(self, url, api_url: str) -> None:
        self.url = url
        self.api_url = api_url

    def parse_data(self) -> None:
        session_obj = requests.Session()

        response = session_obj.get(self.url)
        content = response.text
        table_start = content.index('id="list"')
        data = re.findall(TABLE_ROW, content[table_start:])
        for tag in data[2:]:
            family_match = re.search(LINK, tag)
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
        data = re.findall(TABLE_ROW, content[table_start:])

        for tag in data[2:]:
            sample_match = re.search(LINK, tag)
            sample = sample_match[sample_match.lastindex].split(".")[0]
            try:
                requests.post(self.api_url, json={"hash": sample, "family": family})
            except Exception as e:
                raise Exception("Sending data to API failed") from e
