from datetime import datetime

from marshmallow import ValidationError


def validate_date_in_future(value):
    """Validate date in future."""
    if value < datetime.now().date():
        raise ValidationError('Target date must be in the future')
