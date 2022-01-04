# Generated by Django 2.1.3 on 2021-05-23 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brawlstarsapp', '0013_auto_20210523_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('tag', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('desc', models.CharField(max_length=100)),
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
                ('map', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=20)),
                ('duration', models.IntegerField()),
                ('trophyChange', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OnlyBattle',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('dateTime', models.DateTimeField()),
                ('mode', models.CharField(max_length=15)),
                ('map', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=20)),
                ('trophyChange', models.IntegerField()),
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
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brawlstarsapp.Club')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerGroupBattle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=10)),
                ('groupBattle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brawlstarsapp.GroupBattle')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brawlstarsapp.Player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerOnlyBattle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('onlyBattle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brawlstarsapp.OnlyBattle')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brawlstarsapp.Player')),
            ],
        ),
        migrations.AddField(
            model_name='groupbattle',
            name='mvp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brawlstarsapp.Player'),
        ),
    ]
