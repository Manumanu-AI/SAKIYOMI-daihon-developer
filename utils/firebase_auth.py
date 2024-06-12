import requests
import json
import uuid
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

firebase_api_key = st.secrets['FIREBASE_API_KEY']
firebase_credentials = st.secrets['FIREBASE_CREDENTIALS']
cred_dict = json.loads(firebase_credentials)
cred = credentials.Certificate(cred_dict)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestoreの初期化
db = firestore.client()

def sign_in(email, password):
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

def sign_up(email, password, display_name, role, instagram_username):
    try:
        url = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={firebase_api_key}'
        payload = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }
        response = requests.post(url, data=json.dumps(payload))
        if response.status_code == 200:
            user_id = response.json().get('localId')
            create_user(user_id, email, display_name, role, instagram_username)
            print(f'Successfully created user: {user_id}')
            return response.json()
        else:
            return None
    except Exception as e:
        print(f'Error creating user: {e}')
        return None

def create_user(user_id, email, display_name, role, instagram_username):
    user_data = {
        'user_id': user_id,
        'email': email,
        'display_name': display_name,
        'role': role,
        'created_at': firestore.SERVER_TIMESTAMP,
        'instagram_username': instagram_username
    }
    db.collection('users').document(user_id).set(user_data)

def get_user_info(id_token):
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={firebase_api_key}'
    payload = {
        'idToken': id_token
    }
    response = requests.post(url, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        return None