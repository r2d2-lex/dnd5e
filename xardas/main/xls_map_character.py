# Format (DB_name_field, XLS_cell, options)
from .models.character import CHARACTER_NAME_FIELD, AVATAR_FIELD, ALLIES_AND_ORG_SYMBOL_FIELD

FIRST_PAGE_RECORDS = (
    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 1st page TOP ) -------------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    ('level', 'P4'),
    ('char_history', 'AC4'),
    ('playername', 'AP4'),
    (CHARACTER_NAME_FIELD, 'C4'),
    ('races', 'P7'),
    ('world_view', 'AC7'),
    ('expirence', 'AP7'),

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 1st page 1 column ) --------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #

    # -------------------- (( ХАРАКТЕРИСТИКИ )) ------------------------------------------------------
    ('strength', 'G12'),
    ('strength_modifier', 'K12'),
    ('dexterity', 'G13'),
    ('dexterity_modifier', 'K13'),
    ('constitution', 'G14'),
    ('constitution_modifier', 'K14'),
    ('intellegence', 'G15'),
    ('intellegence_modifier', 'K15'),
    ('wisdom', 'G16'),
    ('wisdom_modifier', 'K16'),
    ('chrarisma', 'G17'),
    ('chrarisma_modifier', 'K17'),

    ('inspiration', 'P15'),
    ('prof_bonus', 'P12'),

    # -------------------- (( СПАСБРОСКИ )) ----------------------------------------------------------
    ('st_strength', 'AK24'),
    ('st_dexterity', 'AK25'),
    ('st_constitution', 'AK26'),
    ('st_intellegence', 'AK27'),
    ('st_wisdom', 'AK28'),
    ('st_chrarisma', 'AK29'),
    ('st_strength_box', 'AM24'),
    ('st_dexterity_box', 'AM25'),
    ('st_constitution_box', 'AM26'),
    ('st_intellegence_box', 'AM27'),
    ('st_wisdom_box', 'AM28'),
    ('st_chrarisma_box', 'AM29'),

    # -------------------- (( НАВЫКИ )) ---------------------------------------------------------------
    ('acrobatics_box', 'M21'),
    ('animal_box', 'M25'),
    ('arcana_box', 'Z21'),
    ('athletics_box', 'M22'),
    ('deception_box', 'Z23'),
    ('history_box', 'M28'),
    ('insight_box', 'Z25'),
    ('intimidation_box', 'M26'),
    ('investigation_box', 'Z26'),
    ('nature_box', 'Z24'),
    ('performance_box', 'M27'),
    ('medicine_box', 'Z22'),
    ('perception_box', 'M23'),
    ('persuasion_box', 'Z29'),
    ('religion_box', 'Z27'),
    ('sleight_of_hand_box', 'M29'),
    ('stealth_box', 'Z28'),
    ('survival_box', 'M24'),

    ('psv_perception', 'C32'),
    ('prof_and_languages', 'C35'),

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 1st page 2 column ) --------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    ('armor_class', 'AL12'),
    ('initiative', 'AL13'),
    ('speed', 'AL14'),

    ('hit_points_curr', 'AL15'),
    ('hit_points_max', 'AL17'),

    ('hit_points_temp', 'AL16'),

    ('hit_dice', 'P18'),
    ('hit_dice_total', ''),

    # -------------------- (( Спасброски от смерти )) ----------------------------------------------------
    ('st_succ_death_box1', 'AI20'),
    ('st_succ_death_box2', 'AK20'),
    ('st_succ_death_box3', 'AM20'),
    ('st_fail_death_box1', 'AI21'),
    ('st_fail_death_box2', 'AK21'),
    ('st_fail_death_box3', 'AM21'),

    ('attacks_and_spell_casting', 'P37'),

    ('equipment', 'T44'),
    ('gold_count', 'R47'),
    ('silver_count', 'R46'),
    ('copper_count', 'R45'),

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 1st page 3 column ) --------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    ('pers_traits', 'AP12'),
    ('ideals', 'AP18'),
    ('bonds', 'AP24'),
    ('flaws', 'AP30'),
    ('features_traits', 'AP36'),
)

IMAGE_SIZES = {
    AVATAR_FIELD: (280, 280),
    ALLIES_AND_ORG_SYMBOL_FIELD: (280, 280),
}

SECOND_PAGE_RECORDS = (
    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 2 page TOP) ----------------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    (CHARACTER_NAME_FIELD, 'C4'),
    ('age', 'P4'),
    ('height', 'AC4'),
    ('weight', 'AP4'),

    ('eyes', 'P7'),
    ('skin', 'AC7'),
    ('hair', 'AP7'),

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 2 page 1st column) ---------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    (AVATAR_FIELD, 'C12'),
    ('char_backstory', 'C26'),

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 2 page 2 column) ------------------------------------------ #
    # ------------------------------------------------------------------------------------------------ #
    ('allies_and_org', 'U12'),
    ('allies_and_org_symbol_name', 'AO12'),
    (ALLIES_AND_ORG_SYMBOL_FIELD, 'AO15'),
    ('additional_features_traits', 'U26'),
    ('treasure', 'U48'),
)

THIRD_PAGE_RECORDS = (
    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 3 page ) -------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    # name + char_classes
    ('spell_casting_ability', 'P4'),
    ('spell_save_dc', 'AC4'),
    ('spell_attack_bonus', 'AP4'),

    # Третье поле в кортеже заклинаний это уровень и индекс заклинаний
    # Уровень 0
    ('spells', 'D10', '0,0'),
    ('spells', 'D11', '0,1'),
    ('spells', 'D12', '0,2'),
    ('spells', 'D13', '0,3'),
    ('spells', 'D14', '0,4'),
    ('spells', 'D15', '0,5'),
    ('spells', 'D16', '0,6'),
    ('spells', 'D17', '0,7'),
    ('spells', 'D18', '0,8'),

    # Уровень 1
    ('spells', 'D22', '1,0'),
    ('spells', 'D23', '1,1'),
    ('spells', 'D24', '1,2'),
    ('spells', 'D25', '1,3'),
    ('spells', 'D26', '1,4'),
    ('spells', 'D27', '1,5'),
    ('spells', 'D28', '1,6'),
    ('spells', 'D29', '1,7'),
    ('spells', 'D30', '1,8'),
    ('spells', 'D31', '1,9'),
    ('spells', 'D32', '1,10'),
    ('spells', 'D33', '1,11'),

    # Уровень 2
    ('spells', 'D37', '2,0'),
    ('spells', 'D38', '2,1'),
    ('spells', 'D39', '2,2'),
    ('spells', 'D40', '2,3'),
    ('spells', 'D41', '2,4'),
    ('spells', 'D42', '2,5'),
    ('spells', 'D43', '2,6'),
    ('spells', 'D44', '2,7'),
    ('spells', 'D45', '2,8'),
    ('spells', 'D46', '2,9'),
    ('spells', 'D47', '2,10'),
    ('spells', 'D48', '2,11'),
    ('spells', 'D49', '2,12'),
    ('spells', 'D50', '2,13'),
    ('spells', 'D51', '2,14'),
    ('spells', 'D52', '2,15'),
    ('spells', 'D53', '2,16'),

    # Уровень 3
    ('spells', 'V10', '3,0'),
    ('spells', 'V11', '3,1'),
    ('spells', 'V12', '3,2'),
    ('spells', 'V13', '3,3'),
    ('spells', 'V14', '3,4'),
    ('spells', 'V15', '3,5'),
    ('spells', 'V16', '3,6'),
    ('spells', 'V17', '3,7'),
    ('spells', 'V18', '3,8'),
    ('spells', 'V19', '3,9'),
    ('spells', 'V20', '3,10'),
    ('spells', 'V21', '3,11'),
    ('spells', 'V22', '3,12'),

    # Уровень 4
    ('spells', 'V26', '4,0'),
    ('spells', 'V27', '4,1'),
    ('spells', 'V28', '4,2'),
    ('spells', 'V29', '4,3'),
    ('spells', 'V30', '4,4'),
    ('spells', 'V31', '4,5'),
    ('spells', 'V32', '4,6'),
    ('spells', 'V33', '4,7'),
    ('spells', 'V34', '4,8'),
    ('spells', 'V35', '4,9'),
    ('spells', 'V36', '4,10'),
    ('spells', 'V37', '4,11'),
    ('spells', 'V38', '4,12'),

    # Уровень 5
    ('spells', 'V42', '5,0'),
    ('spells', 'V43', '5,1'),
    ('spells', 'V44', '5,2'),
    ('spells', 'V45', '5,3'),
    ('spells', 'V46', '5,4'),
    ('spells', 'V47', '5,5'),
    ('spells', 'V48', '5,6'),
    ('spells', 'V49', '5,7'),
    ('spells', 'V50', '5,8'),
    ('spells', 'V51', '5,9'),
    ('spells', 'V52', '5,10'),
    ('spells', 'V53', '5,11'),

    # Уровень 6
    ('spells', 'AN10', '6,0'),
    ('spells', 'AN11', '6,1'),
    ('spells', 'AN12', '6,2'),
    ('spells', 'AN13', '6,3'),
    ('spells', 'AN14', '6,4'),
    ('spells', 'AN15', '6,5'),
    ('spells', 'AN16', '6,6'),
    ('spells', 'AN17', '6,7'),
    ('spells', 'AN18', '6,8'),
    ('spells', 'AN19', '6,9'),
    ('spells', 'AN20', '6,10'),
    ('spells', 'AN21', '6,11'),
    ('spells', 'AN22', '6,12'),

    # Уровень 7
    ('spells', 'AN26', '7,0'),
    ('spells', 'AN27', '7,1'),
    ('spells', 'AN28', '7,2'),
    ('spells', 'AN29', '7,3'),
    ('spells', 'AN30', '7,4'),
    ('spells', 'AN31', '7,5'),
    ('spells', 'AN32', '7,6'),
    ('spells', 'AN33', '7,7'),
    ('spells', 'AN34', '7,8'),
    ('spells', 'AN35', '7,9'),
    ('spells', 'AN36', '7,10'),

    # Уровень 8
    ('spells', 'AN40', '8,0'),
    ('spells', 'AN41', '8,1'),
    ('spells', 'AN42', '8,2'),
    ('spells', 'AN43', '8,3'),
    ('spells', 'AN44', '8,4'),
    ('spells', 'AN45', '8,5'),

    # Уровень 9
    ('spells', 'AN49', '9,0'),
    ('spells', 'AN50', '9,1'),
    ('spells', 'AN51', '9,2'),
    ('spells', 'AN52', '9,3'),
    ('spells', 'AN53', '9,4'),

)

CHARACTER_FORM_RECORDS = (FIRST_PAGE_RECORDS,  SECOND_PAGE_RECORDS, THIRD_PAGE_RECORDS)
