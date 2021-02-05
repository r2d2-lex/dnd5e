from collections import namedtuple
from .pdf_processing import ProcessPdf
from .utilites import get_date_time
import os


class BaseKeyNotFound(KeyError):
    pass


class ExportPDF:
    def __init__(self, char):
        self.char = char
        self.pdf_name = self.get_pdf_name()

    def generate_pdf(self):
        data = self.make_form_data()
        pdf = ProcessPdf()
        data_pdf = pdf.add_data_to_pdf('main/templates/pdf/form2.pdf', data)
        print('Pdf ok...')
        return self.pdf_name, data_pdf

    def make_form_data(self):
        data = {}
        PDF_FORM = namedtuple('PDF_RECORDS', 'pdf_field db_field type description')
        for _record in PDF_FORM_RECORDS:
            record = PDF_FORM(*_record)
            if record.db_field:
                print(r'PDF_field: "{}", DB_field: "{}"'.format(record.pdf_field, record.db_field))
                value = self.get_db_value(record.db_field)
                if value:
                    data[record.pdf_field] = [value, record.type]
        print(data)
        return data

    def get_pdf_name(self):
        charname = self.get_db_value('name')
        if not charname:
            raise BaseKeyNotFound
        part_name = get_date_time('%Y%m%d')
        return charname+part_name+'.pdf'

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


PDF_FORM_RECORDS = (
    # 1'st page
    ('ClassLevel', 'level', 'string', 'класс и уровень'),
    ('Background', '', 'string', 'предыстория'),
    ('PlayerName', 'playername', 'string', ''),
    ('CharacterName', 'name', 'string', ''),
    ('Race', 'races', 'string', 'раса'),
    ('Alignment', 'world_view', 'string', 'мировозрение'),
    ('XP', 'expirence', 'string', 'опыт'),
    ('Inspiration', 'inspiration', 'string', 'вдохновение'),

    ('STR', 'strength', 'string', 'Сила'),
    ('STRmod', 'strength_modifier', 'string', ''),
    ('DEX', 'dexterity', 'string', ''),
    ('DEXmod', 'dexterity_modifier', 'string', ''),
    ('CON', 'constitution', 'string', ''),
    ('CONmod', 'constitution_modifier', 'string', ''),
    ('WIS', 'wisdom', 'string', ''),
    ('WISmod', 'wisdom_modifier', 'string', ''),
    ('CHA', 'chrarisma', 'string', ''),
    ('CHamod', 'chrarisma_modifier', 'string', ''),
    ('INT', 'intellegence', 'string', ''),
    ('INTmod', 'intellegence_modifier', 'string', ''),

    ('ProfBonus', 'prof_bonus', 'string', 'Бонус мастерства'),
    ('AC', 'armor_class', 'string', 'Класс доспеха'),
    ('Initiative', 'initiative', 'string', 'инициатива'),
    ('Speed', 'speed', 'string', 'Скорость персонажа'),

    ('PersonalityTraits', 'pers_traits', 'string', 'Персональные черты'),
    ('Ideals', 'ideals', 'string', 'идеалы'),
    ('Bonds', 'bonds', '', 'Привязанности'),
    ('Flaws', 'flaws', 'string', 'Пороки'),

    ('Check Box 12', '', 'checkbox', 'спас броски от смерти'),
    ('Check Box 13', '', 'checkbox', 'спас броски от смерти'),
    ('Check Box 14', '', 'checkbox', 'спас броски от смерти'),
    ('Check Box 15', '', 'checkbox', 'спас броски от смерти'),
    ('Check Box 16', '', 'checkbox', 'спас броски от смерти'),
    ('Check Box 17', '', 'checkbox', 'спас броски от смерти'),

    ('HD', 'hitpoints_str', 'string', 'кость хитов Current'),
    ('HDTotal', '', 'string', 'кость хитов MAX'),
    ('HPMax', 'hitpoints_max', 'string', 'Максимум хитов'),
    ('HPCurrent', 'hitpoints_curr', 'string', 'текущие хиты'),
    ('HPTemp', 'hitpoints_temp', 'string', 'временные хиты'),

    ('ST Strength', '', '', 'спасбросок силы'),
    ('ST Dexterity', '', '', 'спасбросок знч'),
    ('ST Constitution', '', '', 'спасбросок знч'),
    ('ST Intelligence', '', '', 'спасбросок знч'),
    ('ST Wisdom', '', '', 'спасбросок знч'),
    ('ST Charisma', '', '', 'спасбросок знч'),
    ('Check Box 11', '', 'checkbox', 'спасбросок чекбокс'),
    ('Check Box 18', '', 'checkbox', 'спасбросок чекбокс'),
    ('Check Box 19', '', 'checkbox', 'спасбросок чекбокс'),
    ('Check Box 20', '', 'checkbox', 'спасбросок чекбокс'),
    ('Check Box 21', '', 'checkbox', 'спасбросок чекбокс'),
    ('Check Box 22', '', 'checkbox', 'спасбросок чекбокс'),

    ('Acrobatics', '', '', 'Акробатика(лов)'),
    ('Animal', '', '', 'Анализ(инт)'),
    ('Athletics', '', '', 'broken'),
    ('Deception', '', '', 'broken'),
    ('History', '', '', 'broken'),
    ('Insight', '', '', 'broken'),
    ('Intimidation', '', '', 'broken'),
    ('Investigation', '', '', 'broken'),
    ('Arcana', '', '', 'broken'),
    ('Perception', '', '', 'broken'),
    ('Nature', '', '', 'broken'),
    ('Performance', '', '', 'broken'),
    ('Medicine', '', '', 'broken'),
    ('Persuasion', '', '', 'broken'),
    ('Religion', '', '', 'broken'),
    ('SleightofHand', '', '', 'broken'),
    ('Stealth', '', '', 'broken'),
    ('Survival', '', '', 'broken'),
    ('Check Box 23', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 24', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 25', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 26', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 27', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 28', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 29', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 30', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 31', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 32', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 33', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 34', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 35', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 36', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 37', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 38', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 39', '', 'checkbox', 'чекбокс навыков'),
    ('Check Box 40', '', 'checkbox', 'чекбокс навыков'),

    ('AttacksSpellcasting', '', '', 'атаки и заклинания'),
    ('Wpn Name', '', '', 'атаки и закл. название1'),
    ('Wpn1 AtkBonus', '', '', 'атаки и закл. бонус атаки1'),
    ('Wpn1 Damage', '', '', 'атаки и закл. урон/вид1'),
    ('Wpn Name 2', '', '', 'атаки и закл. название2'),
    ('Wpn2 AtkBonus', '', '', 'атаки и закл. бонус атаки2'),
    ('Wpn2 Damage', '', '', 'атаки и закл. урон/вид2'),
    ('Wpn Name 3', '', '', 'атаки и закл. название3'),
    ('Wpn3 AtkBonus', '', '', 'атаки и закл. бонус атаки3'),
    ('Wpn3 Damage', '', '', 'атаки и закл. урон/вид3'),

    ('Passive', '', 'string', 'пассивная мудрость (внимательность)'),

    ('ProficienciesLang', '', 'string', 'прочие владения и языки'),
    ('Equipment', '', 'string', 'снаряжение'),
    ('CP', 'copper_count', 'string', 'медные монеты'),
    ('SP', 'silver_count', 'string', 'серебряные монеты'),
    ('EP', '', 'string', 'монеты?'),
    ('GP', 'gold_count', 'string', 'золотые монеты'),
    ('PP', '', 'string', 'платиновые монеты?'),
    ('Features and Traits', '', 'string', 'умения и особенности'),
    # 2 page
    ('CharacterName 2', 'name', 'string', 'имя на втором листе'),
    ('Age', 'age', 'string', ''),
    ('Height', 'height', 'string', ''),
    ('Weight', 'weight', 'string', ''),
    ('Eyes', 'eyes', 'string', ''),
    ('Skin', 'skin', 'string', ''),
    ('Hair', 'hair', 'string', ''),
    ('Allies', '', 'string', 'союзники и организации'),
    ('FactionName', '', 'string', 'имя организации'),
    ('Faction Symbol Image', '', 'image', 'символ организации'),
    ('Backstory', '', 'string', 'предыстроия персонажа'),
    ('Feat+Traits', '', '', 'доп. умения и особенности'),
    ('Treasure', '', '', 'сокровища'),
    # 3'rd page
    ('Spellcasting Class 2', '', '', 'класс заклинателя'),
    ('SpellcastingAbility 2', '', '', 'базовая хар-ка'),
    ('SpellSaveDC  2', '', '', 'сила спасения'),
    ('SpellAtkBonus 2', '', '', 'бонус атаки заклинанием'),
)

SPELL_LEVELS = {
    0: (
        # Spells 0 level
        ('Spells 1014', '', '', ''),
        ('Spells 1016', '', '', ''),
        ('Spells 1017', '', '', ''),
        ('Spells 1018', '', '', ''),
        ('Spells 1019', '', '', ''),
        ('Spells 1020', '', '', ''),
        ('Spells 1021', '', '', ''),
        ('Spells 1022', '', '', ''),
    ),
    1: (
        # Spells 1 level
        ('SlotsTotal 19', '', '', ''),
        ('SlotsRemaining 19', '', '', ''),
        ('Spells 1015', '', '', ''),
        ('Spells 1023', '', '', ''),
        ('Spells 1024', '', '', ''),
        ('Spells 1025', '', '', ''),
        ('Spells 1026', '', '', ''),
        ('Spells 1027', '', '', ''),
        ('Spells 1028', '', '', ''),
        ('Spells 1029', '', '', ''),
        ('Spells 1030', '', '', ''),
        ('Spells 1031', '', '', ''),
        ('Spells 1032', '', '', ''),
        ('Spells 1033', '', '', ''),
    ),
    2: (
        ('SlotsTotal 20', '', '', ''),
        ('SlotsRemaining 20', '', '', ''),
        ('Spells 1034', '', '', ''),
        ('Spells 1035', '', '', ''),
        ('Spells 1036', '', '', ''),
        ('Spells 1037', '', '', ''),
        ('Spells 1038', '', '', ''),
        ('Spells 1039', '', '', ''),
        ('Spells 1040', '', '', ''),
        ('Spells 1041', '', '', ''),
        ('Spells 1042', '', '', ''),
        ('Spells 1043', '', '', ''),
        ('Spells 1044', '', '', ''),
        ('Spells 1045', '', '', ''),
        ('Spells 1046', '', '', ''),
    ),
    3: (
        ('SlotsTotal 21', '', '', ''),
        ('SlotsRemaining 21', '', '', ''),
        ('Spells 1047', '', '', ''),
        ('Spells 1048', '', '', ''),
        ('Spells 1049', '', '', ''),
        ('Spells 1050', '', '', ''),
        ('Spells 1051', '', '', ''),
        ('Spells 1052', '', '', ''),
        ('Spells 1053', '', '', ''),
        ('Spells 1054', '', '', ''),
        ('Spells 1055', '', '', ''),
        ('Spells 1056', '', '', ''),
        ('Spells 1057', '', '', ''),
        ('Spells 1058', '', '', ''),
        ('Spells 1059', '', '', ''),
    ),
    4: (
        ('SlotsTotal 22', '', '', ''),
        ('SlotsRemaining 22', '', '', ''),
        ('Spells 1060', '', '', ''),
        ('Spells 1061', '', '', ''),
        ('Spells 1062', '', '', ''),
        ('Spells 1063', '', '', ''),
        ('Spells 1064', '', '', ''),
        ('Spells 1065', '', '', ''),
        ('Spells 1066', '', '', ''),
        ('Spells 1067', '', '', ''),
        ('Spells 1068', '', '', ''),
        ('Spells 1069', '', '', ''),
        ('Spells 1070', '', '', ''),
        ('Spells 1071', '', '', ''),
        ('Spells 1072', '', '', ''),
    ),
    5: (
        ('SlotsTotal 23', '', '', ''),
        ('SlotsRemaining 23', '', '', ''),
        ('Spells 1073', '', '', ''),
        ('Spells 1074', '', '', ''),
        ('Spells 1075', '', '', ''),
        ('Spells 1076', '', '', ''),
        ('Spells 1077', '', '', ''),
        ('Spells 1078', '', '', ''),
        ('Spells 1079', '', '', ''),
        ('Spells 1080', '', '', ''),
        ('Spells 1081', '', '', ''),
    ),
    6: (
        ('SlotsTotal 24', '', '', ''),
        ('SlotsRemaining 24', '', '', ''),
        ('Spells 1082', '', '', ''),
        ('Spells 1083', '', '', ''),
        ('Spells 1084', '', '', ''),
        ('Spells 1085', '', '', ''),
        ('Spells 1086', '', '', ''),
        ('Spells 1087', '', '', ''),
        ('Spells 1088', '', '', ''),
        ('Spells 1089', '', '', ''),
        ('Spells 1090', '', '', ''),
    ),
    7: (
        ('SlotsTotal 25', '', '', ''),
        ('SlotsRemaining 25', '', '', ''),
        ('Spells 1091', '', '', ''),
        ('Spells 1092', '', '', ''),
        ('Spells 1093', '', '', ''),
        ('Spells 1094', '', '', ''),
        ('Spells 1095', '', '', ''),
        ('Spells 1096', '', '', ''),
        ('Spells 1097', '', '', ''),
        ('Spells 1098', '', '', ''),
        ('Spells 1099', '', '', ''),
    ),
    8: (
        ('SlotsTotal 26', '', '', ''),
        ('SlotsRemaining 26', '', '', ''),
        ('Spells 10100', '', '', ''),
        ('Spells 10101', '', '', ''),
        ('Spells 10102', '', '', ''),
        ('Spells 10103', '', '', ''),
        ('Spells 10104', '', '', ''),
        ('Spells 10105', '', '', ''),
        ('Spells 10106', '', '', ''),
    ),
    9: (
        ('SlotsTotal 27', '', '', ''),
        ('SlotsRemaining 27', '', '', ''),
        ('Spells 10107', '', '', ''),
        ('Spells 10108', '', '', ''),
        ('Spells 10109', '', '', ''),
        ('Spells 101010', '', '', ''),
        ('Spells 101011', '', '', ''),
        ('Spells 101012', '', '', ''),
        ('Spells 101013', '', '', ''),
    ),
}

# ('Check Box 314', '', '', ''),
# ('Check Box 3031', '', '', ''),
# ('Check Box 3032', '', '', ''),
# ('Check Box 3033', '', '', ''),
# ('Check Box 3034', '', '', ''),
# ('Check Box 3035', '', '', ''),
# ('Check Box 3036', '', '', ''),
# ('Check Box 3037', '', '', ''),
# ('Check Box 3038', '', '', ''),
# ('Check Box 3039', '', '', ''),
# ('Check Box 3040', '', '', ''),
# ('Check Box 321', '', '', ''),
# ('Check Box 320', '', '', ''),
# ('Check Box 3060', '', '', ''),
# ('Check Box 3061', '', '', ''),
# ('Check Box 3062', '', '', ''),
# ('Check Box 3063', '', '', ''),
# ('Check Box 3064', '', '', ''),
# ('Check Box 3065', '', '', ''),
# ('Check Box 3066', '', '', ''),
# ('Check Box 315', '', '', ''),
# ('Check Box 3041', '', '', ''),
# ('Check Box 251', '', '', ''),
# ('Check Box 309', '', '', ''),
# ('Check Box 3010', '', '', ''),
# ('Check Box 3011', '', '', ''),
# ('Check Box 3012', '', '', ''),
# ('Check Box 3013', '', '', ''),
# ('Check Box 3014', '', '', ''),
# ('Check Box 3015', '', '', ''),
# ('Check Box 3016', '', '', ''),
# ('Check Box 3017', '', '', ''),
# ('Check Box 3018', '', '', ''),
# ('Check Box 3019', '', '', ''),
# ('Check Box 323', '', '', ''),
# ('Check Box 322', '', '', ''),
# ('Check Box 3067', '', '', ''),
# ('Check Box 3068', '', '', ''),
# ('Check Box 3069', '', '', ''),
# ('Check Box 3070', '', '', ''),
# ('Check Box 3071', '', '', ''),
# ('Check Box 3072', '', '', ''),
# ('Check Box 3073', '', '', ''),
# ('Check Box 317', '', '', ''),
# ('Check Box 316', '', '', ''),
# ('Check Box 3042', '', '', ''),
# ('Check Box 3043', '', '', ''),
# ('Check Box 3044', '', '', ''),
# ('Check Box 3045', '', '', ''),
# ('Check Box 3046', '', '', ''),
# ('Check Box 3047', '', '', ''),
# ('Check Box 3048', '', '', ''),
# ('Check Box 3049', '', '', ''),
# ('Check Box 3050', '', '', ''),
# ('Check Box 3051', '', '', ''),
# ('Check Box 3052', '', '', ''),
# ('Check Box 325', '', '', ''),
# ('Check Box 324', '', '', ''),
# ('Check Box 3074', '', '', ''),
# ('Check Box 3075', '', '', ''),
# ('Check Box 3076', '', '', ''),
# ('Check Box 3077', '', '', ''),
# ('Check Box 3078', '', '', ''),
# ('Check Box 313', '', '', ''),
# ('Check Box 310', '', '', ''),
# ('Check Box 3020', '', '', ''),
# ('Check Box 3021', '', '', ''),
# ('Check Box 3022', '', '', ''),
# ('Check Box 3023', '', '', ''),
# ('Check Box 3024', '', '', ''),
# ('Check Box 3025', '', '', ''),
# ('Check Box 3026', '', '', ''),
# ('Check Box 3027', '', '', ''),
# ('Check Box 3028', '', '', ''),
# ('Check Box 3029', '', '', ''),
# ('Check Box 3030', '', '', ''),
# ('Check Box 319', '', '', ''),
# ('Check Box 318', '', '', ''),
# ('Check Box 3053', '', '', ''),
# ('Check Box 3054', '', '', ''),
# ('Check Box 3055', '', '', ''),
# ('Check Box 3056', '', '', ''),
# ('Check Box 3057', '', '', ''),
# ('Check Box 3058', '', '', ''),
# ('Check Box 3059', '', '', ''),
# ('Check Box 327', '', '', ''),
# ('Check Box 326', '', '', ''),
# ('Check Box 3079', '', '', ''),
# ('Check Box 3080', '', '', ''),
# ('Check Box 3081', '', '', ''),
# ('Check Box 3082', '', '', ''),
# ('Check Box 3083', '', '', ''),
