from .base import *
import dj_database_url

DEBUG = False 

DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": env("SUPABASE_ACCESS_KEY_ID"),
            "secret_key": env("SUPABASE_SECRET_ACCESS_KEY"),
            "bucket_name": env("SUPABASE_BUCKET_NAME"),
            "region_name": env("SUPABASE_REGION"),
            "endpoint_url": env("SUPABASE_ENDPOINT_URL"),
            "default_acl": "public-read",
            "file_overwrite": False,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": env("SUPABASE_ACCESS_KEY_ID"),
            "secret_key": env("SUPABASE_SECRET_ACCESS_KEY"),
            "bucket_name": env("SUPABASE_STATIC_BUCKET_NAME"),
            "region_name": env("SUPABASE_REGION"),
            "endpoint_url": env("SUPABASE_ENDPOINT_URL"),
            "default_acl": "public-read",
            "file_overwrite": False,
            "location": "static",  
        },
    },
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
