from urllib.parse import unquote
import uuid
from time import sleep
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn, DownloadColumn
from rich.panel import Panel

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
    
    def progress_bar(self):
        console = Console()
        return Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                DownloadColumn(binary_units=True),
                TimeRemainingColumn(),
                TransferSpeedColumn(),
                console=console
            )


    def download(self):
        filename = self.details['filename']

        console = Console()
        console.print()
        panel = Panel(f"Downloading {filename}", title="Cinema")
        console.print(panel)

        filePath = self.get_file_path()

        console.print()
        
        with self.progress_bar() as progress:

            task = progress.add_task(description=f"[green]{filename}", total=self.details['total_size'])

            with open(f'{filePath}/{self.details['filename']}', 'wb') as file:
                for chunk in self.response.iter_content(chunk_size=8192):
                    if chunk:
                        size = file.write(chunk)
                        progress.update(task, advance=size)
                        sleep(0.01)
        
        console.print()

        console.print(f"Successfully installed [red]{filename}[/red] to [green]{filePath}")

        console.print()
        
