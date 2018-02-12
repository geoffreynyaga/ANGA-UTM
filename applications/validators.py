from datetime import datetime, date, timedelta

from django.core.exceptions import ValidationError

def validate_start_date(value):
    if (value - date.today()).total_seconds() < 0:
        raise ValidationError('You cant book a flight before TODAY!!')
    else:
        return value
