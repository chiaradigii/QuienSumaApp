# applications/comunicaciones/templatetags/custom_filters.py

from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def custom_date(value):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    value_date = value.date()

    if value_date == today:
        return f"Hoy {value.strftime('%H:%M')}"
    elif value_date == yesterday:
        return f"Ayer {value.strftime('%H:%M')}"
    else:
        return value.strftime('%d %b %Y %H:%M')
