from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import CUSTOM_ID_PARAMS, USER_MAX__URL_LENGTH
from .error_handlers import InvalidAPIError, ShortIDAlreadyExistsError
from .models import URLMap


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link_by_id(short_id):
    urlmap = URLMap.get_short_id_from_db(short_id)

    if urlmap is None:
        raise InvalidAPIError('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify({'url': urlmap.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIError('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIError('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if custom_id:
        if (len(custom_id) > USER_MAX__URL_LENGTH or not
                CUSTOM_ID_PARAMS.fullmatch(custom_id)):
            raise InvalidAPIError(
                'Указано недопустимое имя для короткой ссылки')

    try:
        urlmap = URLMap.get_unique_short_id(data['url'], custom_id or None)
    except ShortIDAlreadyExistsError:
        raise InvalidAPIError(
            'Предложенный вариант короткой ссылки уже существует.')

    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED
