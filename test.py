from rich.console import Console 
from tqdm import tqdm
from time import sleep

console = Console()

json_data = '''
[
    {"name": "Movie A", "year": 2020, "rating": 8.2},
    {"name": "Movie B", "year": 2021, "rating": 7.5},
    {"name": "Movie C", "year": 2019, "rating": 9.0}
]
'''

# console.print_json(json_data)

# console.rule("Downloading Acrimony.mp4")

# t = tqdm(total=1000, unit='iB', unit_scale=True, unit_divisor=1024, colour="green")

# with console.status("Downloading...", spinner="dots"):
#     for i in range(5):
#         console.log(f"Found {i} digits")
#         sleep(5)
