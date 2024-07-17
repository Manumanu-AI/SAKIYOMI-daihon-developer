from firebase_admin import firestore
from domain.canva_template import CanvaTemplate
from typing import Dict, Any, List
from config.firebase import db

class CanvaTemplateRepository:
    def create_canva_template(self, template: CanvaTemplate) -> Dict[str, Any]:
        doc_ref = db.collection('common_canva_templates').document(template.id)
        doc_ref.set(template.dict())
        return {'status': 'success', 'template_id': template.id}

    def read_canva_template(self, template_id: str) -> Dict[str, Any]:
        doc_ref = db.collection('common_canva_templates').document(template_id)
        doc = doc_ref.get()
        if doc.exists:
            return {'status': 'success', 'template': doc.to_dict()}
        else:
            return {'status': 'error', 'message': 'Template not found'}

    def update_canva_template(self, template: CanvaTemplate) -> Dict[str, Any]:
        doc_ref = db.collection('common_canva_template').document(template.id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update(template.dict(exclude_unset=True))
            return {'status': 'success', 'template_id': template.id}
        else:
            return {'status': 'error', 'message': 'Template not found'}

    def delete_canva_template(self, template_id: str) -> Dict[str, Any]:
        doc_ref = db.collection('common_canva_templates').document(template_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.delete()
            return {'status': 'success', 'template_id': template_id}
        else:
            return {'status': 'error', 'message': 'Template not found'}

    def list_canva_templates(self) -> Dict[str, Any]:
        docs = db.collection('common_canva_templates').stream()
        templates = [doc.to_dict() for doc in docs]
        return templates
