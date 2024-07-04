from firebase_admin import firestore
from domain.user_index import UserIndex
from typing import Dict, Any
from config.firebase import db

class UserIndexRepository:
    def create_user_index(self, user_index: UserIndex) -> Dict[str, Any]:
        doc_ref = db.collection('users').document(user_index.user_id).collection('user_index').document(user_index.type)
        doc_ref.set(user_index.dict())
        return {'status': 'success', 'index_id': user_index.index_id}

    def read_user_index(self, user_id: str, type: str) -> Dict[str, Any]:
        doc_ref = db.collection('users').document(user_id).collection('user_index').document(type)
        doc = doc_ref.get()
        if doc.exists:
            return {'status': 'success', 'data': doc.to_dict()}
        else:
            return {'status': 'error', 'message': 'Document not found'}

    def update_user_index(self, user_index: UserIndex) -> Dict[str, Any]:
        doc_ref = db.collection('users').document(user_index.user_id).collection('user_index').document(user_index.type)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update(user_index.dict(exclude_unset=True))
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Document not found'}

    def delete_user_index(self, user_id: str, type: str) -> Dict[str, Any]:
        doc_ref = db.collection('users').document(user_id).collection('user_index').document(type)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.delete()
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Document not found'}

    def list_user_indices(self, user_id: str) -> Dict[str, Any]:
        docs = db.collection('users').document(user_id).collection('user_index').stream()
        return {'status': 'success', 'data': [{'index_id': doc.id, **doc.to_dict()} for doc in docs]}
