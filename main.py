import argparse
import requests
from Downloader import Downloader
from Formatter import Formatter
from auth.authentication import Authentication

base_url = "http://localhost:8000"

def create_parser():
    parser = argparse.ArgumentParser(description="Download movies and series through the terminal")
    sub_parsers = parser.add_subparsers(dest="command")

    all_parser = sub_parsers.add_parser("latest", help="The latest titles")

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

def latest(token):

    formatter = Formatter()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(f'{base_url}/latest/', headers=headers)
    except requests.exceptions.RequestException:
        print()
        formatter.format_rule("Connection Error")
        formatter.format_error("Failed to establish connection to the server. Check your internet connection or please try again later!")
        print()
    else:
        if response.status_code == 200:
            formatter.format_rule("Latest titles")
            formatter.format_table(response.json())

def get_details(args, token):

    formatter = Formatter()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    if args.movie:
        # get movie details
        try:
            response = requests.get(f'{base_url}/details/movie/{args.machine_name}/', headers=headers)
        except requests.exceptions.RequestException:
            print()
            formatter.format_rule("Connection Error")
            formatter.format_error("Failed to establish connection to the server. Check your internet connection or please try again later!")
            print()
        else:
            if response.status_code == 404:
                formatter.format_rule("Error")
                formatter.format_error(response.json()['detail'])
            else:
                formatter.format_rule(f"Details: {args.machine_name}")
                formatter.format_details(response.json())
    elif args.serie:
        # get serie details
        try:
            response = requests.get(f'{base_url}/details/serie/{args.machine_name}/', headers=headers)
        except requests.exceptions.RequestException:
            print()
            formatter.format_rule("Connection Error")
            formatter.format_error("Failed to establish connection to the server. Check your internet connection or please try again later!")
            print()
        else:
            if response.status_code == 404:
                formatter.format_rule("Error")
                formatter.format_error(response.json()['detail'])
            else:        
                formatter.format_rule(f"Details: {args.machine_name}")
                formatter.format_details(response.json())
    else:
        return None 
    
def search(args, token):

    formatter = Formatter()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(f'{base_url}/search/?query={args.query}', headers=headers)
    except requests.exceptions.RequestException:
        print()
        formatter.format_rule("Connection Error")
        formatter.format_error("Failed to establish connection to the server. Check your internet connection or please try again later!")
        print()
    else:
        if response.status_code == 404:
            formatter.format_rule("Error")
            formatter.format_error(response.json()['detail'])
        else:
            formatter.format_rule(f"Search: {args.query}")
            formatter.format_table(response.json())

def download(args, token):

    formatter = Formatter()

    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    if args.movie:
        try:
            response = requests.get(f'{base_url}/download/movie/{args.machine_name}', headers=headers)
        except requests.exceptions.RequestException:
            print()
            formatter.format_rule("Connection Error")
            formatter.format_error("Failed to establish connection to the server. Check your internet connection or please try again later!")
            print()
        else:
            if response.status_code == 404:
                formatter.format_rule("Error")
                formatter.format_error(response.json()['detail'])
            else:
                downloader = Downloader(response, "movie")
                downloader.download()
        
    elif args.serie:
        machine_name = args.machine_name
        season = input("Season: ")
        try:
            season = int(season)
        except ValueError:
            formatter.format_error("Please enter a valid digit and try again!")
        else:
            episode = input("Episode: ")
            try:
                episode = int(episode)
            except ValueError:
                formatter.format_error("Please enter a valid digit and try again!")
            else:
                try:
                    response = requests.get(f'{base_url}/download/serie/{machine_name}?season={season}&episode={episode}', headers=headers)
                except requests.exceptions.RequestException:
                    print()
                    formatter.format_rule("Connection Error")
                    formatter.format_error("Failed to establish connection to the server. Check your internet connection or please try again later!")
                    print()
                else:
                    if response.status_code == 404:
                        formatter.format_rule("Error")
                        formatter.format_error(response.json()['detail'])
                    else:
                        downloader = Downloader(response, "serie")
                        downloader.download()

        
def main():
    parser = create_parser()
    args = parser.parse_args()

    authentication = Authentication()
    token = authentication.get_token()

    if token:
        if args.command == "latest":
            latest(token)
        elif args.command == "details":
            get_details(args, token)
        elif args.command == "search":
            search(args, token)
        elif args.command == "download":
            download(args, token)
        else:
            parser.print_help()
    
if __name__=='__main__':
    main()
