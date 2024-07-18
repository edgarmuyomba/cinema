from rich.console import Console
from rich.table import Table
from rich import box

class Formatter:
    def __init__(self):
        self.console = Console()

    def format_table(self, response):
        table = Table(box=box.SQUARE)
        table.add_column("Name", style="cyan", header_style="cyan")
        table.add_column("Machine Name", style="magenta", header_style="magenta")
        table.add_column("Director", style="green_yellow", header_style="green_yellow")
        table.add_column("Themes", style="dark_orange", header_style="dark_orange")
        table.add_column("Year", style="plum1", header_style="plum1")
        table.add_column("Type")

        for row in response:
            table.add_row(row['name'], row['machine_name'], row['director'], row['themes'], str(row['year']), row['type'])

        self.console.print(table)

    def format_details(self, response):
        table = Table(box=box.SQUARE)
        table.add_column("Name", style="cyan", header_style="cyan")
        table.add_column("Machine Name", style="magenta", header_style="magenta")
        table.add_column("Director", style="green_yellow", header_style="green_yellow")
        table.add_column("Cast", style="yellow2", header_style="yellow2")
        table.add_column("Length", style="green", header_style="green")
        table.add_column("Plot", style="deep_pink2", header_style="deep_pink2")
        table.add_column("Themes", style="dark_orange", header_style="dark_orange")
        table.add_column("Year", style="plum1", header_style="plum1")

        
        table.add_row(response['name'], response['machine_name'], response['director'], response['cast'], f"{str(response['length'])} minutes", response['plot'], response['themes'], str(response['year']))

        self.console.print(table)

    def format_error(self, error_message):
        self.console.print(f" {error_message} ", style="white on red")

    def format_rule(self, text):
        self.console.rule(text)
