from flask_wtf import FlaskForm, RecaptchaField

from wtforms import StringField, TextAreaField
from wtforms.fields.html5 import IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.widgets.html5 import NumberInput, HiddenInput

from .utils import (
    get_user_choices,
    get_client_choices,
    get_product_areas_choices
)


class FeatureRequestForm(FlaskForm):
    id = IntegerField(
        validators=[Optional()],
        widget=HiddenInput()
    )
    title = StringField(
        label='Title',
        validators=[DataRequired(), Length(max=255)]
    )
    description = TextAreaField(
        label='Description',
        render_kw={'rows': 5},
        validators=[Optional()]
    )
    user = QuerySelectField(
        label='User',
        get_label='name',
        validators=[DataRequired()],
        query_factory=get_user_choices
    )
    client = QuerySelectField(
        label='Client',
        get_label='name',
        validators=[DataRequired()],
        query_factory=get_client_choices
    )
    feature_priority = IntegerField(
        default=1,
        label='Feature priority',
        validators=[Optional()],
        widget=NumberInput(step=1, min=1)
    )
    product_area = QuerySelectField(
        get_label='name',
        label='Product Area',
        validators=[DataRequired()],
        query_factory=get_product_areas_choices
    )
    captcha = RecaptchaField()
