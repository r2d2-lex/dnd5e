from django.db import models


class ClassManager(models.Manager):
    """ Создание таблицы с классами персонажей """

    def create_db(self):
        # Удаляем все записи перед созданием...
        for records_to_remove in self.all():
            records_to_remove.delete()

        for rc in CharClasses.CLASS_CHOICES:
            self.create(name=rc[0], caption=rc[1], description='Описание класса ' + rc[1])
        return


# Таблица класса персонажа
class CharClasses(models.Model):
    CLASS_CHOICES = (
        ('Варвар', "Варвар"),
        ('Бард', "Бард"),
        ('Жрец', "Жрец"),
        ('Друид', "Друид"),
        ('Воин', "Воин"),
        ('Монах', "Монах"),
        ('Паладин', "Паладин"),
        ('Следопыт', "Следопыт"),
        ('Плут', "Плут"),
        ('Чародей', "Чародей"),
        ('Колдун', "Колдун"),
        ('Волшебник', "Волшебник"),
    )
    name = models.CharField(db_index=True, choices=CLASS_CHOICES, unique=True, null=False, max_length=20,
                            verbose_name='Имя класса персонажа')
    caption = models.CharField(null=True, max_length=24, verbose_name='Caption класса')
    description = models.CharField(null=True, max_length=1024 * 64, verbose_name='Описание класса')
    char_classes = ClassManager()
    objects = models.Manager()

    @staticmethod
    def get_classes_captions():
        """
         Получение описаний классов...
         Возвращает список из двух элементов: Имя, Описание
        """
        return [(cl_name, cl_caption) for cl_name, cl_caption in CharClasses.CLASS_CHOICES]

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'main'


class RaceManager(models.Manager):
    # Класс модели всегда доступен управляющему классу через
    # self.model.
    def get_races(self):
        return self.values_list('name', flat=True).order_by('name')

    """ Создание таблицы с рассами персонажей """

    def create_db(self):
        # Удаляем все записи перед созданием...
        for records_to_remove in self.all():
            records_to_remove.delete()

        for rc in CharRaces.RACE_CHOICES:
            self.create(name=rc[0], caption=rc[1], description='Описание рассы ' + rc[1])
        return


class CharRaces(models.Model):
    RACE_CHOICES = (
        ('dwarf', "Дварф"),
        ('elf', "Эльф"),
        ('half', "Полурослик"),
        ('human', "Человек"),
        ('dragon', "Драконорождённый"),
        ('gnom', "Гном"),
        ('halfelf', "Полуэльф"),
        ('halfork', "Полуорк"),
        ('tifling', "Тифлинг"),
    )
    name = models.CharField(db_index=True, choices=RACE_CHOICES, unique=True, null=False, max_length=20,
                            verbose_name='Имя рассы персонажа')
    caption = models.CharField(null=True, max_length=24, verbose_name='Caption рассы')
    description = models.CharField(null=True, max_length=1024 * 64, verbose_name='Описание рассы')

    char_races = RaceManager()
    objects = models.Manager()

    @staticmethod
    def get_races_captions():
        """
         Получение описаний расс...
         Возвращает список из двух элементов: Имя рассы, Описание рассы
        """
        return [(race_name, race_caption) for race_name, race_caption in CharRaces.RACE_CHOICES]

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'main'
