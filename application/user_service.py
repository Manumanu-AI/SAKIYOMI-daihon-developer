import requests
from infrastructure.user_repository import UserRepository
from domain.user import User
from typing import Dict, Any
import json
from config.firebase import db, firebase_api_key

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def sign_up_user(self, email: str, password: str, display_name: str, instagram_username: str) -> Dict[str, Any]:
        user = User(
            user_id='',
            email=email,
            display_name=display_name,
            role='user',
            instagram_username=instagram_username
        )
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
