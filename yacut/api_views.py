from flask import jsonify, request

from . import app
from .constants import CUSTOM_ID_PARAMS
from .error_handlers import InvalidAPIError
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()

    if urlmap is None:
        raise InvalidAPIError('Указанный id не найден', 404)

    return jsonify({'url': urlmap.original}), 200


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIError('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIError('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if custom_id:
        if len(custom_id) > 16 or not CUSTOM_ID_PARAMS.fullmatch(custom_id):
            raise InvalidAPIError(
                'Указано недопустимое имя для короткой ссылки')

    short_id = get_unique_short_id(data['url'], custom_id or None)

    if short_id is None:
        raise InvalidAPIError(
            'Предложенный вариант короткой ссылки уже существует.')

    urlmap = URLMap.query.filter_by(short=short_id).first()

    return jsonify(urlmap.to_dict()), 201