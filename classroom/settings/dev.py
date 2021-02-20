DEBUG = True
from .base import REST_FRAMEWORK

ALLOWED_HOSTS = ['localhost','127.0.0.1']

# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']= (
#         'rest_framework.renderers.JSONRenderer',
#     )

CORS_ORIGIN_ALLOW_ALL=True
