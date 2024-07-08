# infrastructure/insight_repository.py

from firebase_admin import firestore
from domain.insight import Insight
from typing import List, Dict, Any
from config.firebase import db
import logging

class InsightRepository:
    def __init__(self):
        self.db = db

    def get_insights_by_user(self, user_id: str) -> List[Insight]:
        insights = []
        user_ref = self.db.collection('users').document(user_id)
        insight_collection = user_ref.collection('insight_data')
        
        logging.info(f"Fetching insights for user: {user_id}")
        
        for doc in insight_collection.stream():
            logging.info(f"Found document: {doc.id}")
            insight_data = doc.to_dict()
            insight_data['post_id'] = doc.id
            insight_data['user_id'] = user_id
            insights.append(Insight.from_dict(insight_data))
        
        logging.info(f"Total insights found: {len(insights)}")
        return insights

    def create_insight(self, insight: Insight) -> Dict[str, Any]:
        user_ref = self.db.collection('users').document(insight.user_id)
        insight_ref = user_ref.collection('insight_data').document(insight.post_id)
        insight_dict = insight.dict()
        insight_dict['created_at'] = firestore.SERVER_TIMESTAMP
        insight_dict['posted_at'] = firestore.SERVER_TIMESTAMP
        insight_ref.set(insight_dict)
        logging.info(f"Created new insight for user {insight.user_id}, post_id: {insight.post_id}")
        return {"status": "success", "message": "New insight created successfully"}

    def update_insight(self, insight: Insight) -> Dict[str, Any]:
        user_ref = self.db.collection('users').document(insight.user_id)
        insight_ref = user_ref.collection('insight_data').document(insight.post_id)
        insight_ref.set(insight.dict())
        logging.info(f"Updated insight for user {insight.user_id}, post_id: {insight.post_id}")
        return {"status": "success", "message": "Insight updated successfully"}

    def get_user_ids(self) -> List[str]:
        users = self.db.collection('users').stream()
        user_ids = [user.id for user in users]
        logging.info(f"Retrieved {len(user_ids)} user IDs")
        return user_ids
