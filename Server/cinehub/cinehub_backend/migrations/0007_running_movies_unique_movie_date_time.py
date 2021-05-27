# Generated by Django 3.2.3 on 2021-05-27 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinehub_backend', '0006_alter_movie_poster'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='running_movies',
            constraint=models.UniqueConstraint(fields=('date', 'time', 'hall_id'), name='unique_movie_date_time'),
        ),
    ]