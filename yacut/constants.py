import os
import re

URL_MAX_LENGTH = 256
URL_MIN_LENGTH = 0
CUSTOM_MAX_LENGTH = 16
DISK_TOKEN = os.getenv('DISK_TOKEN')
CUSTOM_ID_PARAMS = re.compile(r'^[a-zA-Z0-9]+$')
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
REQUEST_UPLOAD_URL = (f'{API_HOST}{API_VERSION}/disk/resources/upload')