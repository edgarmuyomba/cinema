from cryptography.fernet import Fernet
import os
import requests
from getpass import getpass
from ..Formatter import Formatter
import json

base_url = "http://localhost:8000"

class Authentication:
    def __init__(self):
        self.key = None
        if os.path.exists('secret.key'):
            with open('secret.key', 'rb') as key_file:
                self.key = key_file.read()
        else:
            self.key = Fernet.generate_key()
            with open('secret.key', 'wb') as key_file:
                key_file.write(self.key)

        self.cipher_suite = Fernet(self.key)
        self.formatter = Formatter()

    def store_token(self, token: str):
        token_bytes = token.encode('utf-8')
        encrypted_token = self.cipher_suite.encrypt(token_bytes)
        with open('token.enc', 'wb') as token_file:
            token_file.write(encrypted_token)
    
    def get_token(self):
        if os.path.exists('token.enc'):
            with open('token.enc', 'rb') as token_file:
                encrypted_token = token_file.read()
                decrypted_token = self.cipher_suite.decrypt(encrypted_token).decode()
                return decrypted_token
        else:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
                if config['hasAccount']:
                    token = self.login()
                else:
                    token = self.signup()
            if token:
                self.store_token(token)
                with open('config.json', 'w') as  config_file:
                    config = json.dumps({'hasAccount': True})
                    config_file.write(config)
                return token
            return None
    
    def login(self):

        token = None

        while True:
            self.formatter.format_rule("Login")
            username = input("Username: ")
            password = getpass("Password: ")

            body = {
                'username': username,
                'password': password
            }

            response = requests.post(f'{base_url}/accounts/login/', json=body)

            if response.status_code == 200:
                token = response.json()['token']
                break
            elif response.status_code == 400:
                errors = response.json()
                self.formatter.format_rule("Errors")
                for key, value in errors.enumerate:
                    for error in value:
                        self.formatter.format_error(error)
                        if error == "Unable to log in with provided credentials.":
                            token = self.signup()
                            break             
                continue

        if not token:
            self.formatter.format_error("Failed to authenticate. Please try again!")
        
        return token
    
    def signup(self):

        token = None 

        while True:
            self.formatter.format_rule("Signup")
            username = input("Username: ")
            password = getpass("Password: ")

            body = {
                'username': username,
                'password': password
            }

            response = requests.post(f'{base_url}/accounts/signup/', json=body)

            if response.status_code == 200:
                token = response.json()['token']
                break
            elif response.status_code == 400:
                errors = response.json()
                self.formatter.format_rule("Errors")
                for key, value in errors.enumerate:
                    for error in value:
                        self.formatter.format_error(error)
                continue
            else:
                self.formatter.format_error("Failed to authenticate. Please try again!")
                break
        
        return token