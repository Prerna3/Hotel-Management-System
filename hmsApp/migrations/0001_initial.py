# Generated by Django 5.0.1 on 2024-01-16 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('hotel_id', models.IntegerField(primary_key=True, serialize=False)),
                ('hotel_name', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('2 Star', '2 Star'), ('3 Star', '3 Star'), ('4 Star', '4 Star'), ('5 Star', '5 Star')], max_length=100)),
                ('price', models.IntegerField()),
                ('location', models.CharField(choices=[('Mumbai', 'Mumbai'), ('Pune', 'Pune'), ('Bengaluru', 'Bengaluru'), ('Delhi', 'Delhi'), ('Kolkata', 'Kolkata'), ('Jaipur', 'Jaipur'), ('Udaipur', 'Udaipur'), ('Varanasi', 'Varanasi'), ('Chennai', 'Chennai'), ('Ahemdabad', 'Ahemdabad'), ('Patna', 'Patna'), ('Shimla', 'Shimla'), ('Manali', 'Manali'), ('Indore', 'Indore'), ('Lucknow', 'Lucknow')], max_length=100)),
                ('desc', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='hotel_pics')),
            ],
        ),
    ]
