# Generated by Django 3.2.2 on 2021-05-28 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brawlstarsapp', '0031_auto_20210528_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupbattle',
            name='eventId',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='onlybattle',
            name='eventId',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
