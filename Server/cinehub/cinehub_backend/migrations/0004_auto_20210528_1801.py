# Generated by Django 3.2.3 on 2021-05-28 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinehub_backend', '0003_remove_running_movie_occupied_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='running_movie',
            name='occupied_seats',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.DeleteModel(
            name='Reserved_Seat',
        ),
    ]
