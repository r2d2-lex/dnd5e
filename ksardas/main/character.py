# Format (DB_name_field, Type, Description_field, XLS_cell)

CHARACTER_FORM_RECORDS = (
    # 1'st page
    ('playername', 'string', 'Имя игрока', 'AR4'),
    ('level', 'string', 'класс и уровень', 'R4'),
    ('char_history', 'string', 'предыстория', 'AE4'),
    ('name', 'string', 'Имя персонажа', 'D4'),
    ('races', 'string', 'раса', 'R7'),
    ('world_view', 'string', 'мировозрение', 'AE7'),
    ('expirence', 'string', 'опыт', 'AR7'),

    ('strength', 'string', 'Сила', 'h12'),
    ('strength_modifier', 'string', 'Сил. мдф.', 'l12'),
    ('dexterity', 'string', 'Ловкость', 'h13'),
    ('dexterity_modifier', 'string', 'Лов. мдф.', 'l13'),
    ('constitution', 'string', 'Выносливость', 'h14'),
    ('constitution_modifier', 'string', 'Вын. мдф.', 'l14'),
    ('intellegence', 'string', 'Интеллект', 'h15'),
    ('intellegence_modifier', 'string', 'Инт. мдф.', 'l15'),
    ('wisdom', 'string', 'Мудрость', 'h16'),
    ('wisdom_modifier', 'string', 'Муд. мдф.', 'l16'),
    ('chrarisma', 'string', 'Харизма', 'h17'),
    ('chrarisma_modifier', 'string', 'Хар. мдф.', 'l17'),

    ('inspiration', 'string', 'вдохновение', ''),
    ('prof_bonus', 'string', 'Бонус мастерства', ''),
    ('armor_class', 'string', 'Класс доспеха', ''),
    ('initiative', 'string', 'инициатива', ''),
    ('speed', 'string', 'Скорость персонажа', ''),

    ( 'pers_traits', 'string', 'Персональные черты', ''),
    ('ideals', 'string', 'идеалы', ''),
    ('bonds', 'string', 'Привязанности', ''),
    ('flaws', 'string', 'Пороки', ''),

    ('', 'checkbox', 'спас броски от смерти', ''),
    ('', 'checkbox', 'спас броски от смерти', ''),
    ('', 'checkbox', 'спас броски от смерти', ''),
    ('', 'checkbox', 'спас броски от смерти', ''),
    ('', 'checkbox', 'спас броски от смерти', ''),
    ('', 'checkbox', 'спас броски от смерти', ''),

    ('hitpoints_str', 'string', 'кость хитов Current', ''),
    ('', 'string', 'кость хитов MAX', ''),
    ('hitpoints_max', 'string', 'Максимум хитов', ''),
    ('hitpoints_curr', 'string', 'текущие хиты', ''),
    ('hitpoints_temp', 'string', 'временные хиты', ''),

    ('st_strength', 'string', 'спасбросок силы', ''),
    ('st_dexterity', 'string', 'спасбросок знч', ''),
    ('st_constitution', 'string', 'спасбросок знч', ''),
    ('st_intellegence', 'string', 'спасбросок знч', ''),
    ('st_wisdom', 'string', 'спасбросок знч', ''),
    ('st_chrarisma', 'string', 'спасбросок знч', ''),
    ('st_strength_box', 'checkbox', 'спасбросок чекбокс', ''),
    ('st_dexterity_box', 'checkbox', 'спасбросок чекбокс', ''),
    ('st_constitution_box', 'checkbox', 'спасбросок чекбокс', ''),
    ('st_intellegence_box', 'checkbox', 'спасбросок чекбокс', ''),
    ('st_wisdom_box', 'checkbox', 'спасбросок чекбокс', ''),
    ('st_chrarisma_box', 'checkbox', 'спасбросок чекбокс', ''),

    ('', '', 'Акробатика(лов)', ''),
    ('', '', 'Анализ(инт)', ''),

    ('attacks_spellc', 'string', 'атаки и заклинания', ''),
    ('psv_perception', 'string', 'пассивная мудрость (внимательность)', ''),

    ('profi_languages', 'string', 'прочие владения и языки', ''),
    ('equipment', 'string', 'снаряжение', ''),
    ('copper_count', 'string', 'медные монеты', ''),
    ('silver_count', 'string', 'серебряные монеты', ''),
    ('', 'string', 'монеты?', ''),
    ('gold_count', 'string', 'золотые монеты', ''),
    ('', 'string', 'платиновые монеты?', ''),
    ('features_traits', 'string', 'умения и особенности', ''),

    # 2 list
    ( 'name', 'string', 'имя на втором листе', ''),
    ('age', 'string', '', ''),
    ('height', 'string', '', ''),
    ('weight', 'string', '', ''),
    ('eyes', 'string', '', ''),
    ('skin', 'string', '', ''),
    ('hair', 'string', '', ''),
    ('', 'string', 'союзники и организации', ''),
    ('', 'string', 'имя организации', ''),
    ('', 'image', 'символ организации', ''),
    ('', 'string', 'предыстроия персонажа', ''),
    ('', '', 'доп. умения и особенности', ''),
    ('', '', 'сокровища', ''),

    # 3  page
    ('', '', 'класс заклинателя', ''),
    ('', '', 'базовая хар-ка', ''),
    ('', '', 'сила спасения', ''),
    ('', '', 'бонус атаки заклинанием', ''),
)