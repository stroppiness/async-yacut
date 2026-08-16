import os
import re

URL_MAX_LENGTH = 256
URL_MIN_LENGTH = 0
MAX_SHORT_URL_LENGTH = 6
MAX_ITERATIONS = 10
USER_MAX__URL_LENGTH = 16
DISK_TOKEN = os.getenv('DISK_TOKEN')
CUSTOM_ID_PARAMS = re.compile(r'^[a-zA-Z0-9]+$')
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
REQUEST_UPLOAD_URL = (f'{API_HOST}{API_VERSION}/disk/resources/upload')
SYMBOLS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
FORBIDDEN_URL_NAME = ['files']
