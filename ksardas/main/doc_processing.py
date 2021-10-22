import io
from collections import namedtuple
from django.conf import settings
from .character import CHARACTER_FORM_RECORDS
from docxtpl import DocxTemplate
from .utilites import get_date_time


class BaseKeyNotFound(KeyError):
    pass


class ExportDOC:
    DOCUMENT_EXTENSION = '.docx'
    CONTENT_TYPE = 'application/doc'

    def __init__(self, char):
        self.char = char
        self.doc_name = self.get_doc_name()

    def generate_doc(self):
        context = self.make_form_data()
        doc = DocxTemplate(settings.DOC_TEMPLATE_PATH)
        doc.render(context)
        docx_file = io.BytesIO()
        doc.save(docx_file)
        docx_file.seek(0)
        return self.doc_name, docx_file

    def make_form_data(self):
        data = {}
        DOC_FORM = namedtuple('DOC_RECORDS', 'pdf_field db_field type description')
        for _record in CHARACTER_FORM_RECORDS:
            record = DOC_FORM(*_record)
            if record.db_field:
                print(r'DB_field: "{}", Description: "{}"'.format(record.db_field, record.description))
                value = self.get_db_value(record.db_field)
                if value:
                    data[record.db_field] = value
        print(data)
        return data

    def get_doc_name(self):
        character_name = self.get_db_value('name')
        if not character_name:
            raise BaseKeyNotFound
        part_name = get_date_time('%Y%m%d')
        return character_name+part_name + self.DOCUMENT_EXTENSION

    def get_db_value(self, db_field):
        value = getattr(self.char, db_field)
        if value:
            try:
                value = str(value)
            except TypeError as err:
                print('Bad value: {}'.format(err))
                return False
            print('Value: {}'.format(value))
            return value
