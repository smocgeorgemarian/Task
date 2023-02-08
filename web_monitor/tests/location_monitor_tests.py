import os.path
import unittest

import requests

from web_monitor.location_monitor import LocationMonitor

TESTING_PATH = os.path.join(".", "..", "..", "resources")
API_URL = "http://127.0.0.1:8000"


class MyTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.files = []
        for root, dirs, files in os.walk(TESTING_PATH):
            for file in files:
                self.files.append(os.path.join(root, file))

        family = "Family"
        for index, file in enumerate(self.files):
            if index % 2 == 0:
                continue

            if index % 5 == 0:
                family += 1
            hash_value = LocationMonitor.get_hash_value(file)
            new_url = f"{API_URL}"
            requests.post(url=new_url, json={"hash": hash_value, "family": family})

    def test_smth(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
