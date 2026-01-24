# core/firebase.py
import firebase_admin
from firebase_admin import credentials, db

# Only initialize if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("BusCore/serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": ""
    })
