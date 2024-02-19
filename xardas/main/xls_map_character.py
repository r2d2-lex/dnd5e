# Format (DB_name_field, XLS_cell)
from .models.character import CHARACTER_NAME_FIELD, AVATAR_FIELD, ALLIES_AND_ORG_SYMBOL_FIELD

FIRST_PAGE_RECORDS  = (
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
    ('allies_and_org', ''),
    ('allies_and_org_symbol_name', ''),
    (ALLIES_AND_ORG_SYMBOL_FIELD, 'AO15'),
    ('additional_features_traits', ''),
    ('treasure', ''),
)

THIRD_PAGE_RECORDS = (
    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 3 page ) -------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    # name + char_classes
    ('spell_casting_ability', ''),
    ('spell_save_dc', ''),
    ('spell_attack_bonus', ''),

)

CHARACTER_FORM_RECORDS = ( FIRST_PAGE_RECORDS,  SECOND_PAGE_RECORDS, THIRD_PAGE_RECORDS)
