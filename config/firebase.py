import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebaseの初期化
firebase_api_key = st.secrets['FIREBASE_API_KEY']
firebase_credentials = st.secrets['FIREBASE_CREDENTIALS']
cred_dict = json.loads(firebase_credentials)
cred = credentials.Certificate(cred_dict)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestoreの初期化
db = firestore.client()
