# Generated by Django 4.2.11 on 2024-05-18 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_matchinfodata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchinfodata',
            name='item0',
        ),
        migrations.RemoveField(
            model_name='matchinfodata',
            name='item1',
        ),
        migrations.RemoveField(
            model_name='matchinfodata',
            name='item2',
        ),
        migrations.RemoveField(
            model_name='matchinfodata',
            name='item3',
        ),
        migrations.RemoveField(
            model_name='matchinfodata',
            name='item4',
        ),
        migrations.RemoveField(
            model_name='matchinfodata',
            name='item5',
        ),
        migrations.RemoveField(
            model_name='matchinfodata',
            name='item6',
        ),
        migrations.AddField(
            model_name='matchinfodata',
            name='item',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]