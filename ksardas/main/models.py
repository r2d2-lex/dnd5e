from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import Signal
from .utilites import send_activation_notification


user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True,db_index=True, verbose_name='Прошёл активацию?')
    send_message = models.BooleanField(default=True,verbose_name='Слать сообщение о новых коментариях?')

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username


class CharBase(models.Model):
    owner = models.ForeignKey('AdvUser', null=False, on_delete=models.PROTECT, verbose_name='Владелец персонажа')
    #owner = models.OneToOneField(AdvUser, unique=True, on_delete=models.CASCADE, verbose_name='Владелец персонажа')
    name = models.CharField(db_index=True, null=False, max_length=20, verbose_name='Имя персонажа')
    RACE_CHOICES = (
        ('ELF', "Эльф"),
        ('HUMAN', "Человек"),
        ('DRAGON', "Дракон"),
    )
    race = models.CharField(null=False, choices=RACE_CHOICES, max_length=20, verbose_name='Расса персонажа')
    playername = models.CharField(null=True, max_length=20, verbose_name='Реальное имя персонажа')
    level = models.IntegerField(null=False, default=1, verbose_name='Уровень персонажа')
    expirence = models.IntegerField(null=False, default=0, verbose_name='Опыт персонажа')
    strength = models.IntegerField(null=False, default=8, verbose_name='Сила персонажа')
    dexterity = models.IntegerField(null=False, default=8, verbose_name='Ловкость персонажа')
    constitution = models.IntegerField(null=False, default=8, verbose_name='Телосложение персонажа')
    intellegence = models.IntegerField(null=False, default=8, verbose_name='Интеллект персонажа')
    wisdom = models.IntegerField(null=False, default=8, verbose_name='Мудрость персонажа')
    chrarisma = models.IntegerField(null=False, default=8, verbose_name='Харизма персонажа')
    modified = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время модификации')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-modified']
