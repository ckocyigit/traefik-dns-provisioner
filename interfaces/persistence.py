import yaml
from yaml.loader import SafeLoader

class Persistence():

    def __init__(self, location):
        self.location = location

    def checkFileExistence(self):
        open(self.location, "a")

    def write(self, data):
        self.checkFileExistence()
        with open(self.location, 'w') as f:
            response = yaml.dump(data, f, sort_keys=False, default_flow_style=False)
        return response

    def read(self):
        self.checkFileExistence()
        with open(self.location) as f:
            content = yaml.full_load(f)
        return content

    def saveResponse(self, bulk_id, description, domains, update_url):
        data = {'bulk_id': bulk_id, 
                'description': description, 
                'domains': domains, 
                'update_url': update_url}
        self.write(data)

    def getValue(self, key):
        content = self.read()
        return content[key]

    def setValue(self, key, value):
        content = self.read()
        if not self.hasKey(key):
            self.write({key:value})
        else:
            content[key] = value
        self.write(content)

    def hasKey(self, key):
        content = self.read()
        if content is None: 
            return False
        for k in content:
            if k == key:
                return True
        return False

    def popKey(self, key):
        content = self.read()
        content.pop(key)
        self.write(content)

    def getUpdateURL(self):
        return self.read()['update_url']