from .base import REST_FRAMEWORK

DEBUG = False

ALLOWED_HOSTS = ['ankitm.herokuapp.com']

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']= (
        'rest_framework.renderers.JSONRenderer',
    )

CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:3030',
# ] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
# CORS_ORIGIN_REGEX_WHITELIST = [
#     'http://localhost:3030',
# ]
