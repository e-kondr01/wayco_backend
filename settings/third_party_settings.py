from datetime import timedelta
from decouple import config


# Djanog Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'wayco_back.permissions.CustomDjangoModelPermissions',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Django Rest Framework SimpleJWT

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=180),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=181),
}


# CORS

CORS_ALLOWED_ORIGINS = [config('cors_allowed_origins')]
