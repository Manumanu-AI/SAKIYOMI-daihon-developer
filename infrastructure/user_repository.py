import requests
from firebase_admin import firestore
from domain.user import User
from typing import Dict, Any
import json
from config.firebase import db, firebase_api_key

class UserRepository:
    def create_user(self, user: User, password: str) -> Dict[str, Any]:
        print(user.email)
        try:
            url = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={firebase_api_key}'
            payload = {
                'email': user.email,
                'password': password,
                'returnSecureToken': True
            }
            response = requests.post(url, data=json.dumps(payload))
            if response.status_code == 200:
                user_data = response.json()
                user.user_id = user_data.get('localId')
                user.created_at = firestore.SERVER_TIMESTAMP
                db.collection('users').document(user.user_id).set(user.dict())
                return {'status': 'success', 'user_id': user.user_id}
            else:
                return {'status': 'error', 'message': response.text}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def read_user_by_email(self, email: str) -> Dict[str, Any]:
        try:
            user_query = db.collection('users').where('email', '==', email).limit(1).get()
            if user_query:
                user_doc = user_query[0]
                return {'status': 'success', 'user_data': user_doc.to_dict(), 'user_id': user_doc.id}
            else:
                return {'status': 'error', 'message': 'User not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_user(self, user: User) -> Dict[str, Any]:
        try:
            doc_ref = db.collection('users').document(user.user_id)
            doc_ref.update(user.dict(exclude_unset=True))
            return {'status': 'success', 'user_id': user.user_id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        try:
            db.collection('users').document(user_id).delete()
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def verify_user(self, id_token: str) -> Dict[str, Any]:
        try:
            url = f'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={firebase_api_key}'
            payload = {'idToken': id_token}
            response = requests.post(url, data=json.dumps(payload))
            if response.status_code == 200:
                user_data = response.json()
                user_id = user_data['users'][0]['localId']
                user_doc = db.collection('users').document(user_id).get()
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    return {'status': 'success', 'user_data': user_data}
                else:
                    return {'status': 'error', 'message': 'User not found'}
            else:
                return {'status': 'error', 'message': response.text}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
