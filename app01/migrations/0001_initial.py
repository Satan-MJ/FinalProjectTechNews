# Generated by Django 4.2.4 on 2023-08-31 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('url', models.URLField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('src', models.CharField(max_length=31)),
                ('text', models.TextField()),
                ('html', models.TextField()),
                ('img_src', models.CharField(max_length=31)),
            ],
        ),
    ]
