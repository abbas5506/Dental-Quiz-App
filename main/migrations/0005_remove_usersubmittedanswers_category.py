# Generated by Django 4.1.5 on 2023-02-14 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_usersubmittedanswers_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersubmittedanswers',
            name='category',
        ),
    ]