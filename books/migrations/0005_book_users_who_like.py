# Generated by Django 2.2 on 2020-09-11 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_delete_bookmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='users_who_like',
            field=models.ManyToManyField(related_name='liked_books', to='books.User'),
        ),
    ]
