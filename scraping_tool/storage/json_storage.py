import json
from scraping_tool.storage.base_storage import BaseStorage

class JSONStorage(BaseStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, data):
        with open(self.file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
