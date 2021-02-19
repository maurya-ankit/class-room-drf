from .base import REST_FRAMEWORK

DEBUG = False

ALLOWED_HOSTS = ['ankitm.herokuapp.com']

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']= (
        'rest_framework.renderers.JSONRenderer',
    )


