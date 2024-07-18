from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn, DownloadColumn
from rich.table import Table
from rich.panel import Panel
from rich import box
from time import sleep
import json

console = Console()

console.rule("Search: acr")

table = Table(box=box.SQUARE)
table.add_column("Name", style="cyan", header_style="cyan")
table.add_column("Machine Name", style="magenta", header_style="magenta")
table.add_column("Director", style="green_yellow", header_style="green_yellow")
table.add_column("Themes", style="dark_orange", header_style="dark_orange")
table.add_column("Year", style="plum1", header_style="plum1")
table.add_column("Type")

json_data = '''
[
    {"name": "Acrimony", "machine_name": "acrimony", "director": "Tyler Perry", "themes": "Drama, Horror, Romance", "year": 2018, "type": "movie"},
    {"name": "Acrimony", "machine_name": "acrimony", "director": "Tyler Perry", "themes": "Drama, Horror, Romance", "year": 2018, "type": "movie"},
    {"name": "Acrimony", "machine_name": "acrimony", "director": "Tyler Perry", "themes": "Drama, Horror, Romance", "year": 2018, "type": "movie"},
    {"name": "Acrimony", "machine_name": "acrimony", "director": "Tyler Perry", "themes": "Drama, Horror, Romance", "year": 2018, "type": "movie"}
]
'''


data = json.loads(json_data)

for media in data:
    table.add_row(media['name'], media['machine_name'], media['director'], media['themes'], str(media['year']), media['type'])

console.print(table)

panel = Panel("Downloading Acrimony.mp4", title="Cinema")

console.print(panel)

console.print()

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    DownloadColumn(binary_units=True),
    # FileSizeColumn(),
    TimeRemainingColumn(),
    TransferSpeedColumn(),
    console=console
) as progress:

    task = progress.add_task(description="[green]Acrimony.mp4", total=10000)

    while not progress.finished:
        progress.update(task, advance=1)
        sleep(0.001)

console.print()

console.print("Successfully installed [red]Acrimony.mp4[/red] to [green]/downloads/movie/Acrimony")

console.print(" File not found ", style="white on red")
