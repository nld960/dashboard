import os
from dotenv import load_dotenv

class authentication:
    def __init__(self, auth_type = None):
        load_dotenv()

        if auth_type is None:
            auth_type = str(auth_type)
            
    def _get_client_id_(self):
        self.client_id = os.getenv("CLIENT_ID")
        return self.client_id
            
    def _get_key_(self):
        self.key = os.getenv("KEY")
        return self.key

    def _get_password_(self):
        self.password = os.getenv("PASSWORD")
        return self.password

    def _get_username_(self):
        self.username = os.getenv("USERNAME")
        return self.username