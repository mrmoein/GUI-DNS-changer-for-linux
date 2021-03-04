import json


class Data:
    def __init__(self, path_of_data_file):
        self.default_data = {
            "settings": {"dns": 0, "primary": "", "secondary": ""},
            "dns_list": [
                {
                    "name": "- Default DNS",
                    "primary": "127.0.0.53",
                    "secondary": ""
                },
                {
                    "name": "-- New DNS",
                    "primary": "",
                    "secondary": ""
                },
            ]
        }
        self.path = path_of_data_file
        self.data = {}
        self.read()

    def write(self, data):
        f = open(self.path, 'w')
        f.write(json.dumps(data))
        f.close()

    def read(self):
        try:
            self.data = json.loads(open(self.path, 'r').read())
        except:
            self.write(self.default_data)
            self.data = self.default_data

    def save_changes(self):
        self.write(self.data)