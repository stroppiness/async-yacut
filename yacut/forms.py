from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from .constants import CUSTOM_MAX_LENGTH, URL_MAX_LENGTH, URL_MIN_LENGTH


class YacutForm(FlaskForm):
    original_link = StringField(
        'Введите ссылку, которую желаете сократить.',
        validators=(DataRequired(message='Обязательное поле'),
                    Length(URL_MIN_LENGTH, URL_MAX_LENGTH)),
    )
    custom_id = StringField(
        'Предложите свой вариант короткой ссылки (не более 16 символов)',
        validators=[Length(URL_MIN_LENGTH, CUSTOM_MAX_LENGTH)],
    )


class YacutUploadForm(FlaskForm):
    files = MultipleFileField(
        validators=[DataRequired()]
    )