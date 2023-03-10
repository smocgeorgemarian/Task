import logging
import os
import hashlib
from collections import defaultdict
from time import sleep

import requests

CHUNK_SIZE = 256


class LocationMonitor:
    """
    Location Monitor for creating real time stats

    Needs a wrapper for getting data from different
    storage locations.
    """

    def __init__(self, location: str, api_url: str) -> None:
        self.location = location
        self.api_URL = api_url
        self.families_count = defaultdict(lambda: 0)
        self.total_count = 0
        self.malwares_count = 0

    def get_all_data(self) -> dict:
        for root, dirs, files in os.walk(self.location, topdown=False):
            self.total_count += len(files)
            for file in files:
                full_path = os.path.join(root, file)
                hash_value = self.get_hash_value(full_path=full_path)
                self.add_to_stats(hash_value)

    def add_to_stats(self, hash_value: str) -> None:
        new_URL = f"{self.api_URL}/hashes/{hash_value}"
        response = requests.get(new_URL)
        if response.status_code != 200:
            return
        self.malwares_count += 1
        logging.info(f"File with hash_value {hash_value} found")
        self.families_count[response.content] += 1

    @staticmethod
    def get_hash_value(full_path: str) -> str:
        curr_hash = hashlib.sha256()
        with open(file=full_path, mode='rb') as fd:
            while True:
                content = fd.read(CHUNK_SIZE)
                if content == b'':
                    break
                curr_hash.update(content)
        return curr_hash.hexdigest()

    def __run__(self) -> tuple:
        self.families_count = defaultdict(lambda: 0)
        self.total_count = 0
        self.malwares_count = 0
        try:
            self.get_all_data()
        except Exception as e:
            logging.warning(f"Processing at this step failed due to: {str(e)}")
        else:
            logging.info(f"Stats are: {self.malwares_count}/{self.total_count} are malwares\n"
                         f"Distribution on families:{self.families_count}")
        return self.malwares_count, self.families_count

    def run(self) -> None:
        while True:
            self.__run__()
            sleep(3)
