# Generated by Django 2.0.5 on 2018-06-20 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0011_remove_settingsapp_page_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estimate',
            name='is_sow',
        ),
        migrations.RemoveField(
            model_name='estimate',
            name='is_to',
        ),
        migrations.AddField(
            model_name='estimate',
            name='estimate_types',
            field=models.CharField(blank=True, choices=[('', '---'), ('is_sow', 'Statement of Work'), ('is_to', 'Task Order')], max_length=300, null=True, verbose_name='Estimate types'),
        ),
    ]
