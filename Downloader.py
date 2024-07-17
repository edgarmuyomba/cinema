from urllib.parse import unquote
import uuid
from tqdm import tqdm
from time import sleep
import os

class Downloader:
    def __init__(self, response, type):
        self.response = response 
        self.type = type 
        
        details = {
            "total_size": int(response.headers.get('content-length', 0)),
            "filename": f'{uuid.uuid4}.mp4'
        }

        params = response.headers['Content-Disposition'].split(';')[1:]
        for param in params:
            key, value = param.strip().split('=')
            details[key] = unquote(value.strip('"'))

        self.details = details


    def get_file_path(self):
        if self.type == "movie":
            filepath = f'downloads/movies/{self.details['filename']}'
        elif self.type == "serie":
            season = self.details.get('season', 1)
            name = self.details.get('name')
            filepath = f'downloads/series/{name}/Season {season}'
        else:
            filepath = f'downloads/{self.details['filename']}'
        
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        return filepath
    
    def tqdm_bar(self):
        return tqdm(
                desc=self.details['filename'],
                total=self.details['total_size'],
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
                colour="#67ab3f"
            )


    def download(self):
        filename = self.details['filename']
        print(f"Downloading {filename}")

        filePath = self.get_file_path()
        bar = self.tqdm_bar()

        with open(f'{filePath}/{self.details['filename']}', 'wb') as file:
            for chunk in self.response.iter_content(chunk_size=8192):
                if chunk:
                    size = file.write(chunk)
                    bar.update(size)
                    sleep(0.01)
        
        bar.close()
        print(f"Successfully installed {filename} to {filePath}")