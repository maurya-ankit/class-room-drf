from .base import REST_FRAMEWORK

DEBUG = True

ALLOWED_HOSTS = ['ankitm.herokuapp.com']

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']= (
        'rest_framework.renderers.JSONRenderer',
    )


CORS_ORIGIN_ALLOW_ALL=True
