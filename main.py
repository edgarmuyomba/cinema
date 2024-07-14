import argparse
import requests

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
    search_parser.add_argument('-m','--movie', action='store_true', help="Search for a movie")
    search_parser.add_argument('-s', '--serie', action='store_true', help="Search for a serie")

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
    if args.movie:
        response = requests.get(f'{base_url}/search/movie/?query={args.query}')
        print(response.json())
    elif args.serie:
        response = requests.get(f'{base_url}/search/serie/?query={args.query}')
        print(response.json())
    else:
        return None
    
def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "details":
        get_details(args)
    elif args.command == "search":
        search(args)
    else:
        parser.print_help()
    
if __name__=='__main__':
    main()