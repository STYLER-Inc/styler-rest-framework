"""Firestore config
"""
import os

if os.getenv('ENVIRONMENT') == 'development':
    from mockfirestore import MockFirestore
    CLIENT = MockFirestore()
else:
    from firebase_admin import firestore
    import firebase_admin
    firebase_admin.initialize_app()
    CLIENT = firestore.client()
