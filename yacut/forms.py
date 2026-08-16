from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp

from .constants import USER_MAX__URL_LENGTH, URL_MAX_LENGTH, URL_MIN_LENGTH


class YacutForm(FlaskForm):
    original_link = StringField(
        'Введите ссылку, которую желаете сократить.',
        validators=(DataRequired(message='Обязательное поле'),
                    Length(URL_MIN_LENGTH, URL_MAX_LENGTH)),
    )
    custom_id = StringField(
        'Предложите свой вариант короткой ссылки '
        f'(не более {USER_MAX__URL_LENGTH} символов)',
        validators=[
            Length(URL_MIN_LENGTH, USER_MAX__URL_LENGTH),
            Regexp(r'^[A-Za-z0-9]{0,16}$',
                   message='Только буквы и цифры (0-16 символов)')
        ],
    )


class YacutUploadForm(FlaskForm):
    files = MultipleFileField(
        validators=[DataRequired()]
    )
