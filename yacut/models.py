import datetime

from flask import url_for

from yacut import db

from .constants import URL_MAX_LENGTH


class URLMap(db.Model):
    """Модель для взаимодействия со ссылкой в БД."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_MAX_LENGTH))
    short = db.Column(db.String(URL_MAX_LENGTH), nullable=True)
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.datetime.now)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view',
                short_id=self.short,
                _external=True,
            ),
        )

    def from_dict(self, data):
        self.original = data['url']
        if data.get('custom_id'):
            self.short = data['custom_id']
