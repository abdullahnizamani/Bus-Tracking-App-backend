# core/firebase.py
import firebase_admin
from firebase_admin import credentials, db
from django.conf import settings
import os
path = os.path.join(settings.BASE_DIR, 'serviceAccountKey.json')
# Only initialize if not already initialized
if not firebase_admin._apps:
    if os.path.exists(path):
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://busapp-7d45f-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })
