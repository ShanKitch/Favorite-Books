# Generated by Django 2.2 on 2020-09-11 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_favorite'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookManager',
        ),
    ]