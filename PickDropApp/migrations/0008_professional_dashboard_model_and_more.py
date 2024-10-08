# Generated by Django 5.0.6 on 2024-08-28 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PickDropApp', '0007_user_dashboard_model_dropoff_coords_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='professional_dashboard_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameField(
            model_name='user_dashboard_model',
            old_name='dropoff_coords',
            new_name='dropoff_latitude',
        ),
        migrations.RenameField(
            model_name='user_dashboard_model',
            old_name='pickup_coords',
            new_name='dropoff_longitude',
        ),
        migrations.AddField(
            model_name='user_dashboard_model',
            name='pickup_latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user_dashboard_model',
            name='pickup_longitude',
            field=models.FloatField(default=0),
        ),
    ]
