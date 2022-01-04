# Generated by Django 3.2.2 on 2021-05-26 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brawlstarsapp', '0024_auto_20210523_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupbattle',
            name='mvp',
        ),
        migrations.RemoveField(
            model_name='player',
            name='club',
        ),
        migrations.RemoveField(
            model_name='playergroupbattle',
            name='groupBattle',
        ),
        migrations.RemoveField(
            model_name='playergroupbattle',
            name='player',
        ),
        migrations.RemoveField(
            model_name='playeronlybattle',
            name='onlyBattle',
        ),
        migrations.RemoveField(
            model_name='playeronlybattle',
            name='player',
        ),
        migrations.DeleteModel(
            name='Club',
        ),
        migrations.DeleteModel(
            name='GroupBattle',
        ),
        migrations.DeleteModel(
            name='OnlyBattle',
        ),
        migrations.DeleteModel(
            name='Player',
        ),
        migrations.DeleteModel(
            name='PlayerGroupBattle',
        ),
        migrations.DeleteModel(
            name='PlayerOnlyBattle',
        ),
    ]
