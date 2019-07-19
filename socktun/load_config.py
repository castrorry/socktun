import os
import yaml

class Config(object):
    def __init__(self, file_path=None):
        if file_path is not None:
            self.config = self.load(file_path)
        else:
            default_path = os.path.dirname(os.path.abspath(__file__))
            self.config = self.load(default_path+'/src/default.yaml')
        self.middle_host = self.config["bind"]["host"]
        self.middle_ports = self.config["bind"]["ports"]
        self.dest_host = self.config["destination"]["host"]
        self.dest_port = self.config["destination"]["ports"]
    
    def load(self, path):
        return yaml.safe_load(open(path, 'r'))