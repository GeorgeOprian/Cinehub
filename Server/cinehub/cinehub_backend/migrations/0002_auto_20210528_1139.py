# Generated by Django 3.2.3 on 2021-05-28 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinehub_backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserved_Seat',
            fields=[
                ('reserved_seat', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('seat_number', models.PositiveIntegerField(default=0)),
                ('running', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinehub_backend.running_movie')),
            ],
        ),
        migrations.AddConstraint(
            model_name='reserved_seat',
            constraint=models.UniqueConstraint(fields=('running_id', 'seat_number'), name='unique_reservation_seat'),
        ),
    ]
