# Generated by Django 3.2.2 on 2021-05-26 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brawlstarsapp', '0027_auto_20210526_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('tag', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('desc', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(max_length=15)),
                ('reqTrophies', models.IntegerField()),
                ('trophies', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GroupBattle',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('dateTime', models.DateTimeField()),
                ('mode', models.CharField(max_length=15)),
                ('map', models.CharField(max_length=20, null=True)),
                ('type', models.CharField(max_length=20)),
                ('duration', models.IntegerField()),
                ('trophyChange', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OnlyBattle',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('dateTime', models.DateTimeField()),
                ('mode', models.CharField(max_length=15)),
                ('map', models.CharField(max_length=20, null=True)),
                ('type', models.CharField(max_length=20)),
                ('trophyChange', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('tag', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('trophies', models.IntegerField()),
                ('soloVictories', models.IntegerField()),
                ('duoVictories', models.IntegerField()),
                ('trioVictories', models.IntegerField()),
                ('club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='brawlstarsapp.club')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerOnlyBattle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('brawler', models.CharField(max_length=20)),
                ('onlyBattle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brawlstarsapp.onlybattle')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brawlstarsapp.player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerGroupBattle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=10)),
                ('brawler', models.CharField(max_length=20)),
                ('starPlayer', models.BooleanField()),
                ('groupBattle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brawlstarsapp.groupbattle')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brawlstarsapp.player')),
            ],
        ),
        migrations.AddField(
            model_name='groupbattle',
            name='mvp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brawlstarsapp.player'),
        ),
    ]
