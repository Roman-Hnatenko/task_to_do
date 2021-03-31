import csv
from django import forms
from . import validators


class CsvFileField(forms.FileField):

    def to_python(self, data):

        if not data.content_type == 'text/csv':
            raise forms.ValidationError('File type must be csv')

        csv_file = super().to_python(data)
        decoded_file = csv_file.read().decode().splitlines()
        reader = csv.DictReader(decoded_file)
        return reader


class TaskCsvFileFied(CsvFileField):
    widget=forms.FileInput()
    required_columns = ['Title', 'Description', 'Create Date', 'Complete Date']
    default_validators = [validators.CsvRequiredColumnsValidator(required_columns)]
