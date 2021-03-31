from django.core.exceptions import ValidationError


class CsvRequiredColumnsValidator:
    column_names = ()

    def __init__(self, column_names):
        self.column_names = column_names or self.column_names

    def __call__(self, reader):
        columns = list(set(self.column_names) - set(reader.fieldnames))
        if columns:
            raise ValidationError(f"Missing columns: {', '.join(columns)}")
