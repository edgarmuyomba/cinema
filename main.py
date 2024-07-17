import argparse
import requests
from Downloader import Downloader

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
        if response.status_code == 404:
            print(response.json()['detail'])
        else:
            print(response.json())
    elif args.serie:
        # get serie details
        response = requests.get(f'{base_url}/details/serie/{args.machine_name}/')
        if response.status_code == 404:
            print(response.json()['detail'])
        else:
            print(response.json())
    else:
        return None 
    
def search(args):
    response = requests.get(f'{base_url}/search/?query={args.query}')
    if response.status_code == 404:
        print(response.json()['detail'])
    else:
        print(response.json())

def download(args):
    
    if args.movie:
        response = requests.get(f'{base_url}/download/movie/{args.machine_name}')
        if response.status_code == 404:
            print(response.json()['detail'])
        else:
            downloader = Downloader(response, "movie")
            downloader.download()
        
    elif args.serie:
        machine_name = args.machine_name
        season = input("Season: ")
        try:
            season = int(season)
        except ValueError:
            print("Please enter a valid digit and try again!")
        else:
            episode = input("Episode: ")
            try:
                episode = int(episode)
            except ValueError:
                print("Please enter a valid digit and try again!")
            else:
                response = requests.get(f'{base_url}/download/serie/{machine_name}?season={season}&episode={episode}')
                if response.status_code == 404:
                    print(response.json()['detail'])
                else:
                    downloader = Downloader(response, "serie")
                    downloader.download()

        
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