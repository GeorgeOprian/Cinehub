# Generated by Django 3.2.3 on 2021-05-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinehub_backend', '0004_alter_running_movies_running_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='seats',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='awards',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='released',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
