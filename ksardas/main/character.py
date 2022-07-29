# Format (DB_name_field, Type, Description_field, XLS_cell)

CHARACTER_FORM_RECORDS = (
    # 1'st page top
    ('playername', 'string', 'Имя игрока', 'AR4'),
    ('level', 'string', 'класс и уровень', 'R4'),
    ('char_history', 'string', 'предыстория', 'AE4'),
    ('name', 'string', 'Имя персонажа', 'D4'),
    ('races', 'string', 'раса', 'R7'),
    ('world_view', 'string', 'мировозрение', 'AE7'),
    ('expirence', 'string', 'опыт', 'AR7'),

    # 1'st page 1 column
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

    ('acrobatics', 'string', 'Акробатика(лов)', ''),
    ('animal', 'string', 'Уход за животными(мдр)', ''),
    ('arcana', 'string', 'Магия(инт)', ''),
    ('athletics', 'string', 'Атлетика(сил)', ''),
    ('deception', 'string', 'Обман(хар)', ''),
    ('history', 'string', 'История(инт)', ''),
    ('insight', 'string', 'Проницательность(мдр)', ''),
    ('intimidation', 'string', 'Запугивание(хар)', ''),
    ('investigation', 'string', 'Расследование(инт)', ''),
    ('nature', 'string', 'Природа(инт)', ''),
    ('performance', 'string', 'Выступление(хар)', ''),
    ('medicine', 'string', 'Медицина(мдр)', ''),
    ('perception', 'string', 'Внимательность(мдр.)', ''),
    ('persuasion', 'string', 'Убеждение(хар)', ''),
    ('religion', 'string', 'Религия(инт)', ''),
    ('sleightofHand', 'string', 'Ловкость рук(лов)', ''),
    ('stealth', 'string', 'Скрытность(лов)', ''),
    ('survival', 'string', 'Выживание(мдр)', ''),

    ('psv_perception', 'string', 'пассивная мудрость (внимательность)', ''),

    # 1 st page 2 column
    ('prof_bonus', 'string', 'Бонус мастерства', ''),
    ('initiative', 'string', 'инициатива', ''),
    ('inspiration', 'string', 'вдохновение', ''),
    ('armor_class', 'string', 'Класс доспеха', ''),
    ('speed', 'string', 'Скорость персонажа', ''),

    ('hitpoints_str', 'string', 'кость хитов Current', ''),
    ('', 'string', 'кость хитов MAX', ''),
    ('hitpoints_max', 'string', 'Максимум хитов', ''),
    ('hitpoints_curr', 'string', 'текущие хиты', ''),
    ('hitpoints_temp', 'string', 'временные хиты', ''),


    ('', 'checkbox', 'спас броски от смерти', ''),
    ('', 'checkbox', 'спас броски от смерти', ''),
    ('', 'checkbox', 'спас броски от смерти', ''),
    ('', 'checkbox', 'спас броски от смерти', ''),
    ('', 'checkbox', 'спас броски от смерти', ''),
    ('', 'checkbox', 'спас броски от смерти', ''),

    ('st_strength', 'string', 'спасбросок силы', ''),
    ('st_dexterity', 'string', 'спасбросок ловкость', ''),
    ('st_constitution', 'string', 'спасбросок вынсоливость', ''),
    ('st_intellegence', 'string', 'спасбросок интеллект', ''),
    ('st_wisdom', 'string', 'спасбросок мудрость', ''),
    ('st_chrarisma', 'string', 'спасбросок харизма', ''),
    ('st_strength_box', 'checkbox', 'спасбросок силы', ''),
    ('st_dexterity_box', 'checkbox', 'спасбросок ловкость', ''),
    ('st_constitution_box', 'checkbox', 'спасбросок вынсоливость', ''),
    ('st_intellegence_box', 'checkbox', 'спасбросок интеллект', ''),
    ('st_wisdom_box', 'checkbox', 'спасбросок мудрость', ''),
    ('st_chrarisma_box', 'checkbox', 'спасбросок харизма', ''),


    ('attacks_spellc', 'string', 'Атаки и заклинания', ''),
    ('profi_languages', 'string', 'прочие владения и языки', ''),
    ('equipment', 'string', 'снаряжение', ''),
    ('copper_count', 'string', 'медные монеты', ''),
    ('silver_count', 'string', 'серебряные монеты', ''),
    ('gold_count', 'string', 'золотые монеты', ''),
    ('', 'string', 'other монеты?', ''),
    ('', 'string', 'other монеты?', ''),

    # 1st page 3 column
    ('pers_traits', 'string', 'Персональные черты', ''),
    ('ideals', 'string', 'Идеалы', ''),
    ('bonds', 'string', 'Привязанности', ''),
    ('flaws', 'string', 'Пороки', ''),
    ('features_traits', 'string', 'Умения и особенности', ''),

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