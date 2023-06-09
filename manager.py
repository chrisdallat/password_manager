import os
import json
from cryptography.fernet import Fernet

class passwordManager:
    def __init__(self):
        self.key = None
        self.key_file = "key.key"
        if not os.path.exists(self.key_file):
            with open(self.key_file, 'w') as f:
                self.create_key(self.key_file)
        else: 
            self.load_key(self.key_file)

        self.users = {}
        self.load_data_from_file()

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, "wb") as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, "rb") as f:
            self.key = f.read()

    def encrypt_password(self, password):
        f = Fernet(self.key)
        encrypted_password = f.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(self, encrypted_password):
        f = Fernet(self.key)
        decrypted_password = f.decrypt(encrypted_password).decode()
        return decrypted_password

    def authenticate_user(self, username, password):
        if username in self.users and password == self.decrypt_password(self.users[username]['password']):
            return True
        else:
            return False

    def add_user(self, username, password):
        if username in self.users:
            return False
        else:
            encrypted_password = self.encrypt_password(password)
            self.users[username] = {"password": encrypted_password, "websites": {}}
            self.save_data_to_file()
            self.load_data_from_file()
            return True

    def add_website(self, username, website_name, website_address, website_username, website_password):
        self.load_data_from_file()
        encrypted_password = self.encrypt_password(website_password)
        self.users[username]["websites"][website_name] = {
            "address": website_address,
            "username": website_username,
            "password": encrypted_password
        }
        self.save_data_to_file()

    def edit_website(self, username, website_name, website_address, website_username, website_password):
        self.load_data_from_file()
        encrypted_password = self.encrypt_password(website_password)
        self.users[username]["websites"][website_name] = {
            "address": website_address,
            "username": website_username,
            "password": encrypted_password
        }
        self.save_data_to_file()

    def delete_website(self, username, website_name):
        self.load_data_from_file()
        if website_name not in self.users[username]["websites"]:
            return False
        else:
            del self.users[username]["websites"][website_name]
            self.save_data_to_file()
            return True

    def valid_website_info(self, username, website_name):
        self.load_data_from_file()
        if website_name not in self.users[username]["websites"]:
            try: 
                pass
            except:
                return False
        else:
            return True
        
    def view_website_info(self, username, website_name):
        self.load_data_from_file()
        website = self.users[username]["websites"][website_name]
        return website

    def save_data_to_file(self):
        filename = "passmanager.json"
        data = {}
        for user, info in self.users.items():
            password = info['password'].decode()
            websites = {}
            for website_name, website_info in info['websites'].items():
                website_password = website_info['password'].decode()
                website = {
                    'address': website_info['address'],
                    'username': website_info['username'],
                    'password': website_password
                }
                websites[website_name] = website
            data[user] = {'password': password, 'websites': websites}

            with open(filename, 'w') as f:
                json.dump(data, f)

    def load_data_from_file(self):
        filename = "passmanager.json"
        with open(filename, 'r+') as f:
            try:
                data = json.load(f)
                for username, user_info in data.items():
                    for website_name, website_info in user_info['websites'].items():
                        website_info['password'] = website_info['password'].encode()

                    user_info['password'] = user_info['password'].encode()
                    self.users[username] = user_info
            except:
                data = ""