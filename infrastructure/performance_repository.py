from firebase_admin import firestore
from typing import Dict, Any
from config.firebase import db
from datetime import datetime

class PerformanceRepository:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.collection_ref = db.collection('users').document(user_id).collection('performance')

    def log_run(self, run_type: str, date: datetime.date, count: int = 1) -> Dict[str, Any]:
        date_str = date.strftime('%Y-%m-%d')
        doc_ref = self.collection_ref.document(date_str)
        doc = doc_ref.get()

        if doc.exists:
            doc_ref.update({run_type: firestore.Increment(count)})
        else:
            doc_ref.set({run_type: count})

        return {'status': 'success', 'date': date_str}

    def get_run_count(self, run_type: str, date: datetime.date) -> Dict[str, Any]:
        date_str = date.strftime('%Y-%m-%d')
        doc_ref = self.collection_ref.document(date_str)
        doc = doc_ref.get()

        if doc.exists and run_type in doc.to_dict():
            return {'status': 'success', 'date': date_str, 'count': doc.to_dict()[run_type]}
        else:
            return {'status': 'error', 'message': 'No data found for the specified date and run type'}

    def list_all_runs(self, date: datetime.date) -> Dict[str, Any]:
        date_str = date.strftime('%Y-%m-%d')
        doc_ref = self.collection_ref.document(date_str)
        doc = doc_ref.get()

        if doc.exists:
            return {'status': 'success', 'data': doc.to_dict()}
        else:
            return {'status': 'error', 'message': 'No data found for the specified date'}
