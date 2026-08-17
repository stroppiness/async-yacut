import datetime
import random

from flask import url_for

from yacut import db

from .constants import (URL_MAX_LENGTH, SYMBOLS, MAX_ITERATIONS,
                        FORBIDDEN_URL_NAME, MAX_SHORT_URL_LENGTH)
from .error_handlers import (URLCreationError, ShortIDAlreadyExistsError)


class URLMap(db.Model):
    """Модель для взаимодействия со ссылкой в БД."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_MAX_LENGTH))
    short = db.Column(db.String(URL_MAX_LENGTH), nullable=True)
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.datetime.now)

    def url_preparation(self):
        return url_for(
            'redirect_view',
            short_id=self.short,
            _external=True,
        )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.url_preparation()
        )

    def from_dict(self, data):
        self.original = data['url']
        self.short = data['custom_id']

    @staticmethod
    def db_object_creation(original, short):

        new_object = URLMap(
            original=original,
            short=short,
        )
        db.session.add(new_object)
        db.session.commit()

        return new_object

    @classmethod
    def get_short_id_from_db(cls, short_id):
        return cls.query.filter_by(short=short_id).first()

    @classmethod
    def get_unique_short_id(cls, original_link, custom=None):

        if custom is None:
            short_id = cls.unique_custom_id_generation()
        else:
            short_id = custom

            if (
                cls.get_short_id_from_db(short_id)
                or short_id in FORBIDDEN_URL_NAME
            ):
                raise ShortIDAlreadyExistsError()

        new_short_id = cls.db_object_creation(original_link, short_id)

        return new_short_id

    @classmethod
    def unique_custom_id_generation(cls):
        for _ in range(MAX_ITERATIONS):
            short_id = ''.join(
                random.choices(SYMBOLS,
                               k=MAX_SHORT_URL_LENGTH))

            if not cls.get_short_id_from_db(short_id):
                return short_id

        raise URLCreationError(
            'Не удалось сгенерировать уникальную короткую ссылку'
        )
