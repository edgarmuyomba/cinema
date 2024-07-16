import argparse
import requests
from urllib.parse import unquote
import uuid
from tqdm import tqdm
from time import sleep

base_url = "http://localhost:8000"

def create_parser():
    parser = argparse.ArgumentParser(description="Download movies and series through the terminal")
    sub_parsers = parser.add_subparsers(dest="command")

    details_parser = sub_parsers.add_parser("details", help="Get details about a movie or serie")
    details_parser.add_argument('machine_name', type=str, help="The machine name of the movie or series")
    details_parser.add_argument('-m','--movie', action='store_true', help="Details about a movie")
    details_parser.add_argument('-s', '--serie', action='store_true', help="Details about a serie")

    search_parser = sub_parsers.add_parser("search", help="Find a movie or serie")
    search_parser.add_argument('query', type=str, help="The search query or term")

    download_parser = sub_parsers.add_parser("download", help="Download the movie or series episode")
    download_parser.add_argument('machine_name', type=str, help='The machine name of the movie or serie')
    download_parser.add_argument('-m', '--movie', action='store_true', help='Download a movie')
    download_parser.add_argument('-s', '--serie', action='store_true', help='Download a serie')

    return parser

def get_details(args):
    if args.movie:
        # get movie details
        response = requests.get(f'{base_url}/details/movie/{args.machine_name}/')
        print(response.json())
    elif args.serie:
        # get serie details
        response = requests.get(f'{base_url}/details/serie/{args.machine_name}/')
        print(response.json())
    else:
        return None 
    
def search(args):
    response = requests.get(f'{base_url}/search/?query={args.query}')
    print(response.json())

def download(args):
    if args.movie:
        response = requests.get(f'{base_url}/download/movie/{args.machine_name}')
        total_size = int(response.headers.get('content-length', 0))
        filename = f'{uuid.uuid4}.mp4'
        _, params = response.headers['Content-Disposition'].split(';')
        for param in params.split(';'):
            key, value = param.strip().split('=')
            if key == 'filename':
                filename = unquote(value.strip('"'))
                break
        with open(f'download/movies/{filename}', 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    size = file.write(chunk)
                    bar.update(size)
                    sleep(0.01)
    
def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "details":
        get_details(args)
    elif args.command == "search":
        search(args)
    elif args.command == "download":
        download(args)
    else:
        parser.print_help()
    
if __name__=='__main__':
    main()