from firebase_admin import firestore
from domain.user_index import UserIndex
from typing import Dict, Any
from config.firebase import db

class UserIndexRepository:
    def create_user_index(self, user_index: UserIndex) -> Dict[str, Any]:
        doc_ref = db.collection('users').document(user_index.user_id).collection('user_index').document(user_index.user_id)
        # INFO: 1:1 の参照の簡素化のために、index_id に user_id を設定
        user_index.index_id = user_index.user_id
        doc_ref.set(user_index.dict())
        return {'status': 'success', 'index_id': user_index.user_id}

    def read_user_index(self, user_id: str) -> Dict[str, Any]:
        doc_ref = db.collection('users').document(user_id).collection('user_index').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return {'status': 'success', 'data': doc.to_dict()}
        else:
            return {'status': 'error', 'message': 'Document not found'}

    def update_user_index(self, user_index: UserIndex) -> Dict[str, Any]:
        doc_ref = db.collection('users').document(user_index.user_id).collection('user_index').document(user_index.user_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update(user_index.dict(exclude_unset=True))
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Document not found'}

    def delete_user_index(self, user_id: str) -> Dict[str, Any]:
        doc_ref = db.collection('users').document(user_id).collection('user_index').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.delete()
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Document not found'}
