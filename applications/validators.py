from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta


def validate_start_date(value):
    if (value - date.today()).total_seconds() < 0:
        raise ValidationError('You cant book a flight before TODAY!!')
    else:
        return value
