from firebase_admin import firestore
from domain.instagram_trend_post import InstagramTrendPost
from typing import Dict, Any, List
from config.firebase import db
from datetime import datetime

class InstagramTrendPostRepository:
    def create_post(self, post: InstagramTrendPost) -> Dict[str, Any]:
        post_id = db.collection('instagram_trend_posts').document().id
        post.post_id = post_id

        db.collection('instagram_trend_posts').document(post_id).set(post.dict())
        return {'status': 'success', 'post_id': post_id}

    def create_posts(self, posts: List[InstagramTrendPost]) -> List[Dict[str, Any]]:
        batch = db.batch()
        results = []

        for post in posts:
            post_id = db.collection('instagram_trend_posts').document().id
            post.post_id = post_id
            doc_ref = db.collection('instagram_trend_posts').document(post_id)
            batch.set(doc_ref, post.dict())
            results.append({'status': 'success', 'post_id': post_id})

        batch.commit()
        return results

    def read_post(self, post_id: str) -> Dict[str, Any]:
        doc_ref = db.collection('instagram_trend_posts').document(post_id)
        doc = doc_ref.get()
        if doc.exists:
            return {'status': 'success', 'data': doc.to_dict()}
        else:
            return {'status': 'error', 'message': 'Document not found'}

    def update_post(self, post: InstagramTrendPost) -> Dict[str, Any]:
        doc_ref = db.collection('instagram_trend_posts').document(post.post_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update(post.dict(exclude_unset=True))
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Document not found'}

    def delete_post(self, post_id: str) -> Dict[str, Any]:
        doc_ref = db.collection('instagram_trend_posts').document(post_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.delete()
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Document not found'}

    def list_posts(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        docs = db.collection('instagram_trend_posts')\
            .where('created_at', '>=', start_date)\
            .where('created_at', '<=', end_date).stream()
        return [{'post_id': doc.id, **doc.to_dict()} for doc in docs]
