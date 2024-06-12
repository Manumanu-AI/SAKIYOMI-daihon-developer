from firebase_admin import firestore
from domain.prompt import Prompt
from typing import Dict, Any
from config.firebase import db

class PromptRepository:
    def create_prompt(self, prompt: Prompt) -> Dict[str, Any]:
        doc_ref = db.collection('users').document(prompt.user_id).collection('prompts').document(prompt.type)
        doc_ref.set(prompt.dict())
        return {'status': 'success', 'prompt_id': prompt.prompt_id}

    def read_prompt(self, user_id: str, type: str) -> Dict[str, Any]:
        doc_ref = db.collection('users').document(user_id).collection('prompts').document(type)
        doc = doc_ref.get()
        if doc.exists:
            return {'status': 'success', 'data': doc.to_dict()}
        else:
            return {'status': 'error', 'message': 'Document not found'}

    def update_prompt(self, prompt: Prompt) -> Dict[str, Any]:
        doc_ref = db.collection('users').document(prompt.user_id).collection('prompts').document(prompt.type)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update(prompt.dict(exclude_unset=True))
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Document not found'}

    def delete_prompt(self, user_id: str, type: str) -> Dict[str, Any]:
        doc_ref = db.collection('users').document(user_id).collection('prompts').document(type)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.delete()
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Document not found'}

    def list_prompts(self, user_id: str) -> Dict[str, Any]:
        docs = db.collection('users').document(user_id).collection('prompts').stream()
        return {'status': 'success', 'data': [{'prompt_id': doc.id, **doc.to_dict()} for doc in docs]}
