# Generated by Django 3.2.2 on 2021-05-26 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brawlstarsapp', '0028_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playergroupbattle',
            name='brawler',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='playeronlybattle',
            name='brawler',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
