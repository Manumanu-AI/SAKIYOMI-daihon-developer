import requests
from infrastructure.user_repository import UserRepository
from domain.user import User
from typing import Dict, Any
import json
from config.firebase import db, firebase_api_key

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def create_or_update_user(self, user: User, password: str) -> Dict[str, Any]:
        existing_user_response = self.user_repo.read_user_by_email(user.email)
        print("----------- existing_user_response -----------")
        print(existing_user_response)
        if existing_user_response['status'] == 'success':
            # User exists, update the user information
            user.user_id = existing_user_response['user_id']
            return self.user_repo.update_user(user)
        else:
            # User does not exist, create a new user
            return self.user_repo.create_user(user, password)

    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        try:
            url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}'
            payload = {
                'email': email,
                'password': password,
                'returnSecureToken': True
            }
            response = requests.post(url, data=json.dumps(payload))
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_user_info(self, id_token: str) -> Dict[str, Any]:
        url = f'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={firebase_api_key}'
        payload = {
            'idToken': id_token
        }
        response = requests.post(url, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()
        else:
            return None
