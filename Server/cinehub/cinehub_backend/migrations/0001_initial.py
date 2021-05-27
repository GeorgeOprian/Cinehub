# Generated by Django 3.2.3 on 2021-05-27 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('hall_id', models.AutoField(primary_key=True, serialize=False)),
                ('number_of_seats', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('imdb_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20)),
                ('released', models.CharField(max_length=15)),
                ('duration', models.CharField(max_length=10)),
                ('genre', models.CharField(max_length=100)),
                ('director', models.CharField(max_length=100)),
                ('writer', models.CharField(max_length=100)),
                ('actors', models.CharField(max_length=200)),
                ('plot', models.CharField(max_length=500)),
                ('language', models.CharField(max_length=15)),
                ('awards', models.CharField(max_length=30)),
                ('poster', models.CharField(max_length=250)),
                ('imdb_rating', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Running_movies',
            fields=[
                ('running_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('date', models.CharField(max_length=12)),
                ('time', models.CharField(max_length=5)),
                ('occupied_seats', models.PositiveIntegerField(default=0)),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinehub_backend.hall')),
                ('imdb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinehub_backend.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('seats', models.CharField(max_length=20)),
                ('user_id', models.CharField(max_length=30)),
                ('running', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinehub_backend.running_movies')),
            ],
        ),
        migrations.AddConstraint(
            model_name='running_movies',
            constraint=models.UniqueConstraint(fields=('imdb_id', 'hall_id'), name='unique_movie_hall'),
        ),
    ]