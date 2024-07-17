
from urllib.parse import unquote
import uuid
from tqdm import tqdm
from time import sleep
import os

def handle_download(response):
    total_size = int(response.headers.get('content-length', 0))
    filename = f'{uuid.uuid4}.mp4'
    _, params = response.headers['Content-Disposition'].split(';')
    for param in params.split(';'):
        key, value = param.strip().split('=')
        if key == 'filename':
            filename = unquote(value.strip('"'))
            break
        
    filePath = f'downloads/movies/{filename}'
    if not os.path.exists(filePath):
        os.makedirs(filePath)

    bar = tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
            colour="#67ab3f"
        )

    with open(f'{filePath}/{filename}', 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                size = file.write(chunk)
                bar.update(size)
                sleep(0.01)