# Generated by Django 3.0.2 on 2021-02-12 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210211_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='charbase',
            name='st_chrarisma',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AddField(
            model_name='charbase',
            name='st_chrarisma_box',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='charbase',
            name='st_constitution',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AddField(
            model_name='charbase',
            name='st_constitution_box',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='charbase',
            name='st_dexterity',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AddField(
            model_name='charbase',
            name='st_dexterity_box',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='charbase',
            name='st_intellegence',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AddField(
            model_name='charbase',
            name='st_intellegence_box',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='charbase',
            name='st_strength',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AddField(
            model_name='charbase',
            name='st_strength_box',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='charbase',
            name='st_wisdom',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AddField(
            model_name='charbase',
            name='st_wisdom_box',
            field=models.BooleanField(default=False),
        ),
    ]
