import streamlit as st
import firebase_admin
from firebase_admin import firestore
from datetime import datetime

# Firebaseの初期化（既に初期化されている場合はスキップ）
if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()

def get_insight_data(user_id):
    insight_ref = db.collection('users').document(user_id).collection('insight_data')
    insights = insight_ref.get()
    return [insight.to_dict() for insight in insights]

def main():
    st.title("インサイト分析")
