# jugador/widget.py
from django.forms import DateInput

class DatePickerInput(DateInput):

    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs.update({
            'class': 'form-control datetimepicker-input',
            'data-toggle': 'datetimepicker',
            'data-target': '#id_fecha_nacimiento'  
        })
        super().__init__(attrs=attrs, format='%d-%m-%Y')