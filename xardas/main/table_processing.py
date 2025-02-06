import io
import openpyxl
from collections import namedtuple
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from openpyxl.drawing.image import Image
from loguru import logger
from .xls_map_character import CHARACTER_FORM_RECORDS
from .utilites import get_date_time
from .models.character import CHARACTER_NAME_FIELD

# Высота и ширина ячейки под размер шрифта + отступ
HEIGHT_COEFFICIENT = 1.33
WIDTH_COEFFICIENT = HEIGHT_COEFFICIENT
INDENT_PX = 5


class BaseKeyNotFound(KeyError):
    pass


class ExportXLS:
    DOCUMENT_EXTENSION = '.xlsx'
    CONTENT_TYPE = 'application/doc'

    def __init__(self, char):
        self.char = char
        self.doc_name = self.get_doc_name()
        self.id_file = None
        self.ws = None

    def __enter__(self):
        self.id_file = io.BytesIO()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.id_file:
            self.id_file.close()

    def xls_insert_data(self, context):
        for key, value in context.items():
            try:
                self.ws[key] = value
            except (AttributeError, ValueError) as error:
                logger.error(f'Ошибка шаблона: Ключ: {key} Значение: {value} Ошибка: {error}')

    def get_column_width_in_pixels(self, column_letter):
        column_width = self.ws.column_dimensions[column_letter].width
        if column_width is not None:
            return round(column_width * WIDTH_COEFFICIENT) - INDENT_PX
        return 0

    def get_row_height_in_pixels(self, row):
        row_height = self.ws.row_dimensions[row].height
        if row_height is not None:
            return round(row_height * HEIGHT_COEFFICIENT) - INDENT_PX
        return 0

    def get_merged_cell_dimensions(self, merged_cell_range: str):
        min_col, min_row, max_col, max_row = openpyxl.utils.range_boundaries(merged_cell_range)
        total_width = 0
        for col in range(min_col, max_col + 1):
            column_letter = openpyxl.utils.get_column_letter(col)
            total_width += self.ws.column_dimensions[column_letter].width or 0

        total_height = 0
        for row in range(min_row, max_row + 1):
            total_height += self.ws.row_dimensions[row].height or 0

        total_width_in_pixels = round(total_width * WIDTH_COEFFICIENT) - INDENT_PX
        total_height_in_pixels = round(total_height * HEIGHT_COEFFICIENT) - INDENT_PX
        return total_width_in_pixels, total_height_in_pixels

    def xls_insert_image(self, xls_cell, path_to_image):
        image = openpyxl.drawing.image.Image(path_to_image)

        row = self.ws[xls_cell].row
        column_letter = self.ws[xls_cell].column_letter

        logger.info(
            f'\r\nXls ячейка "{xls_cell}" значение: "{path_to_image}"\r\n'
            f'Номер колонки: "{self.ws[xls_cell].column}"\r\n'
            f'Номер строки: "{row}"\r\n'
            f'Буква строки: "{column_letter}"\r\n'
            f'Путь к изображению: "{path_to_image}"\r\n'
            f'Ширина изображения: "{image.width}"\r\n'
            f'Высота изображения: "{image.height}"'
        )

        # Получаем размеры объединённых ячеек, если ячейка объединена
        merged_cell_range = None
        for merged_range in self.ws.merged_cells.ranges:
            if xls_cell in merged_range:
                merged_cell_range = str(merged_range)
                print(f'Merged cell: {xls_cell} range: {merged_cell_range}')
                break

        if merged_cell_range:
            cell_width_in_pixels, cell_height_in_pixels = self.get_merged_cell_dimensions(merged_cell_range)
            logger.info(
                f'Объединенные размеры ячеек для {merged_cell_range}: ширина в пикселях: {cell_width_in_pixels}, высота в пикселях: {cell_height_in_pixels}')
        else:
            # Если ячейка не объединена, используем обычные методы
            cell_width_in_pixels = self.get_column_width_in_pixels(column_letter)
            cell_height_in_pixels = self.get_row_height_in_pixels(row)

        # растягиваем изображение на ячейку
        image.width = cell_width_in_pixels
        image.height = cell_height_in_pixels
        self.ws.add_image(image, xls_cell)

    def generate_xls(self):
        workbook = openpyxl.load_workbook(settings.XLS_TEMPLATE_PATH)
        sheet_index = 0
        work_book_sheet_names = workbook.sheetnames

        for template_records in CHARACTER_FORM_RECORDS:
            logger.debug(f'Страница: {work_book_sheet_names[sheet_index]}\r\nЗаписи шаблона: {template_records}\r\n')
            # openpyxl.utils.exceptions.InvalidFileException:
            self.ws = workbook[work_book_sheet_names[sheet_index]]
            context = self.make_form_data(template_records)
            self.xls_insert_data(context)

            sheet_index += 1
        workbook.save(self.id_file)
        self.id_file.seek(0)
        return self.doc_name, self.id_file

    '''
        Считываем ячейку из xls_map_character.py и если находим соответствие db_field и xls_cell - помещаем в словарь
    '''
    def make_form_data(self, form_records) -> dict:
        data = {}
        DOC_FORM = namedtuple('DOC_RECORDS', 'db_field xls_cell options')
        for _record in form_records:
            if len(_record) == 3:
                record = DOC_FORM(*_record)
            elif len(_record) == 2:
                record = DOC_FORM(_record[0], _record[1], None)
            else:
                raise ValueError("Неверный формат записи: должно быть 2 или 3 элемента.")

            if record.xls_cell:
                logger.debug(f'DB_field: "{record.db_field}" -> XLS_field: "{record.xls_cell}" -> Options: {record.options}')
                value = self.get_db_value(record.db_field, record.xls_cell, record.options)
                if value:
                    data[record.xls_cell] = value
        return data

    def get_doc_name(self):
        character_name = self.get_db_value(CHARACTER_NAME_FIELD)
        if not character_name:
            raise BaseKeyNotFound
        part_name = get_date_time('%Y%m%d')
        return character_name + part_name + self.DOCUMENT_EXTENSION

    def get_db_value(self, db_field, xls_cell=None, options=None):
        value = ''
        field_type = 'Unknown'
        field_verbose = 'Unknown'

        try:
            field_type = self.get_type_field(db_field)
            field_verbose = self.get_verbose_field(db_field)
        except FieldDoesNotExist as error:
            logger.error(f'Field type error: {db_field} - {error}')

        try:
            value = getattr(self.char, db_field)
        except AttributeError as error:
            logger.error(f'get_db_value error: {error}')

        logger.debug(f'Value: "{value}" Description: "{field_verbose}" Type: "{field_type}"\r\n')

        if field_type == 'BooleanField' and value == True:
            value = '\u2714'  # ✔

        elif field_type == 'ManyToManyField':
            if db_field == 'spells':
                if options:
                    try:
                        spell_level, spell_index = map(int, options.split(','))
                        value = self.char.spells.filter(level=spell_level)[spell_index]
                    except (IndexError, ValueError, TypeError) as error:
                        value = ''
                        logger.debug(f'Ошибка получения опций: {options} {error}')

            if db_field == 'races':
                value = self.char.get_race()

            if db_field == 'char_classes':
                value = self.char.get_current_class()

        elif field_type == 'FileField' and value:
            self.xls_insert_image(xls_cell, value)
            value = ''

        if value:
            try:
                value = str(value)
            except TypeError as err:
                logger.error('Bad value: {}'.format(err))
                return False
            return value

    def get_type_field(self, db_field) -> str:
        result = self.char._meta.get_field(db_field).get_internal_type()
        return result

    def get_verbose_field(self, db_field) -> str:
        result = self.char._meta.get_field(db_field).verbose_name.title()
        return result
