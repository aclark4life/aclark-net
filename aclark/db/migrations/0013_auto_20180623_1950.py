# Generated by Django 2.0.6 on 2018-06-23 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0012_auto_20180620_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estimate',
            name='estimate_types',
        ),
        migrations.AddField(
            model_name='estimate',
            name='estimate_type',
            field=models.CharField(blank=True, choices=[('', '---'), ('is_sow', 'Statement of Work'), ('is_to', 'Task Order')], max_length=300, null=True, verbose_name='Estimate Type'),
        ),
    ]