# infrastructure/insight_repository.py

from firebase_admin import firestore
from domain.insight import Insight
from typing import List, Dict, Any
from config.firebase import db

class InsightRepository:
    def __init__(self):
        self.db = db

    def create_insight(self, insight: Insight) -> Dict[str, Any]:
        doc_ref = self.db.collection('insight_data').document(insight.post_id)
        doc_ref.set(insight.dict())
        return {"status": "success", "message": "New insight created successfully"}

    def get_insights_by_user(self, user_id: str) -> List[Insight]:
        docs = self.db.collection('insight_data').where('user_id', '==', user_id).stream()
        return [Insight.from_dict(doc.to_dict()) for doc in docs]

    def update_insight(self, insight: Insight) -> Dict[str, Any]:
        doc_ref = self.db.collection('insight_data').document(insight.post_id)
        doc_ref.set(insight.dict())
        return {"status": "success", "message": "Insight updated successfully"}
