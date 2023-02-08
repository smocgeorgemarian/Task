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
        self.added_files = []
        for root, dirs, files in os.walk(TESTING_PATH):
            for file in files:
                self.files.append(os.path.join(root, file))

        family = "Family"
        for index, file in enumerate(self.files):
            if index % 2 == 0:
                continue
            self.added_files.append(file)
            hash_value = LocationMonitor.get_hash_value(file)
            new_url = f"{API_URL}"
            requests.post(url=new_url, json={"hash": hash_value, "family": family + str(index)})
        self.monitor = LocationMonitor(api_url=API_URL, location=TESTING_PATH)

    def test_when_db_is_populated_initially(self):
        # Arrange

        # Act
        data = self.monitor.__run__()
        # Assert
        self.assertEqual(2, data[0])
        self.assertEqual(1, data[1][b"Family1"])
        self.assertEqual(1, data[1][b"Family3"])


if __name__ == '__main__':
    unittest.main()
