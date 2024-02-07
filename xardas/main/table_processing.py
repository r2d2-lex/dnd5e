import io
from collections import namedtuple
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from .xls_map_character import CHARACTER_FORM_RECORDS
import openpyxl
from .utilites import get_date_time

CHARACTER_NAME_FIELD = 'character_name'

class BaseKeyNotFound(KeyError):
    pass


def xls_insert_data(ws, context):
    for key, value in context.items():
        try:
            ws[key] = value
        except AttributeError:
            print(f'TEMPLATE ERROR: Key: {key} Value: {value}')


class ExportXLS:
    DOCUMENT_EXTENSION = '.xlsx'
    CONTENT_TYPE = 'application/doc'

    def __init__(self, char):
        self.char = char
        self.doc_name = self.get_doc_name()
        self.id_file = None

    def __enter__(self):
        self.id_file = io.BytesIO()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.id_file:
            self.id_file.close()

    def generate_xls(self):
        context = self.make_form_data()
        # openpyxl.utils.exceptions.InvalidFileException:
        workbook = openpyxl.load_workbook(settings.XLS_TEMPLATE_PATH)
        ws = workbook.active
        xls_insert_data(ws, context)
        workbook.save(self.id_file)
        self.id_file.seek(0)
        return self.doc_name, self.id_file

    def make_form_data(self) -> dict:
        data = {}
        DOC_FORM = namedtuple('DOC_RECORDS', 'db_field xls_cell')
        for _record in CHARACTER_FORM_RECORDS:
            record = DOC_FORM(*_record)
            if record.xls_cell:
                value = self.get_db_value(record.db_field)

                try:
                    field_type = self.get_type_field(record.db_field)
                    field_verbose = self.get_verbose_field(record.db_field)
                except FieldDoesNotExist as error:
                    print(f'{error}')

                print(f'XLS_field: "{record.xls_cell}", Value "{value}" Description: "{field_verbose}" Type: "{field_type}"')

                if field_type == 'BooleanField' and value == 'True':
                    value = '\u2714' # ✔

                if value:
                    data[record.xls_cell] = value
        return data

    def get_doc_name(self):
        character_name = self.get_db_value(CHARACTER_NAME_FIELD)
        if not character_name:
            raise BaseKeyNotFound
        part_name = get_date_time('%Y%m%d')
        return character_name+part_name + self.DOCUMENT_EXTENSION

    def get_db_value(self, db_field):
        value = ''
        try:
            value = getattr(self.char, db_field)
        except AttributeError as error:
            print(f'get_db_value error: {error}')

        if value:
            try:
                value = str(value)
            except TypeError as err:
                print('Bad value: {}'.format(err))
                return False
            print('Value: {}'.format(value))
            return value

    def get_type_field(self, db_field) -> str:
        result = self.char._meta.get_field(db_field).get_internal_type()
        return result

    def get_verbose_field(self, db_field) -> str:
        result = self.char._meta.get_field(db_field).verbose_name.title()
        return result
