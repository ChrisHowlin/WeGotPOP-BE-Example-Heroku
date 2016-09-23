import json
import os

class ArtistFileService:
    def __init__(self, filename):
        self.filename = filename

    def get_artists(self):
        with open(self.filename) as data_file:    
            data = json.load(data_file)
            os.path.dirname(os.path.realpath(__file__))
        return data
