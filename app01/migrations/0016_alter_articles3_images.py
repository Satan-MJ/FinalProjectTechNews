# Generated by Django 4.2.4 on 2023-09-02 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0015_articles3_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles3',
            name='images',
            field=models.TextField(default=';'),
        ),
    ]