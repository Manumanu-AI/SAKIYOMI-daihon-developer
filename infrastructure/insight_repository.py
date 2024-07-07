# infrastructure/insight_repository.py

from firebase_admin import firestore
from domain.insight import Insight
from typing import List, Dict, Any
from config.firebase import db

class InsightRepository:
    def __init__(self):
        self.collection = db.collection('insight_data')

    def get_all_insights(self) -> List[Insight]:
        docs = self.collection.stream()
        return [Insight(**doc.to_dict()) for doc in docs]

    def update_insight(self, insight: Insight) -> Dict[str, Any]:
        doc_ref = self.collection.document(insight.post_id)
        doc_ref.set(insight.dict())
        return {"status": "success", "message": "Insight updated successfully"}

    def get_insights_by_user(self, user_id: str) -> List[Insight]:
        docs = self.collection.where('user_id', '==', user_id).stream()
        return [Insight(**doc.to_dict()) for doc in docs]
