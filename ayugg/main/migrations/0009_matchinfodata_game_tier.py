# Generated by Django 4.2.11 on 2024-05-20 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_matchinfodata_bans'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchinfodata',
            name='game_tier',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
