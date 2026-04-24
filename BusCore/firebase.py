# # core/firebase.py
# import firebase_admin
# from firebase_admin import credentials, db
# from django.conf import settings
# import os
# path = os.path.join(settings.BASE_DIR, 'serviceAccountKey.json')
# # Only initialize if not already initialized
# if not firebase_admin._apps:
#     if os.path.exists(path):
#         cred = credentials.Certificate(path)
#         firebase_admin.initialize_app(cred, {
#             "databaseURL": "https://busapp-7d45f-default-rtdb.asia-southeast1.firebasedatabase.app/"
#         })

import firebase_admin
from firebase_admin import credentials, db
import environ
import json
import base64
import os
from django.conf import settings

env = environ.Env()
path = os.path.join(settings.BASE_DIR, 'BusCore/serviceAccountKey.json')

if not firebase_admin._apps:
    if env('DJANGO_SETTINGS_MODULE') == 'BusCore.settings.development':
        cred = credentials.Certificate(path)
    else:
        service_account = json.loads(base64.b64decode(env("FIREBASE_SERVICE_ACCOUNT")))
        cred = credentials.Certificate(service_account)
    
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://busapp-7d45f-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })