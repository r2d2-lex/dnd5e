# Generated by Django 4.0.6 on 2022-08-16 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_delete_mobbase_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='charbase',
            name='spell_attack_bonus',
            field=models.CharField(default='', max_length=12, verbose_name='Бонус к атаке заклинанием'),
        ),
        migrations.AddField(
            model_name='charbase',
            name='spell_casting_ability',
            field=models.CharField(default='', max_length=12, verbose_name='Характеристика заклинателя'),
        ),
        migrations.AddField(
            model_name='charbase',
            name='spell_save_dc',
            field=models.CharField(default='', max_length=12, verbose_name='DC спасброска от заклинания'),
        ),
    ]
