# Generated by Django 2.0.5 on 2018-05-30 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0010_auto_20180530_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settingsapp',
            name='page_size',
        ),
    ]
