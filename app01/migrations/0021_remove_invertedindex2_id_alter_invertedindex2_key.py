# Generated by Django 4.2.4 on 2023-09-03 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0020_invertedindex2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invertedindex2',
            name='id',
        ),
        migrations.AlterField(
            model_name='invertedindex2',
            name='key',
            field=models.CharField(max_length=31, primary_key=True, serialize=False),
        ),
    ]