# Generated by Django 4.2.4 on 2023-09-02 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0011_delete_sources_articles2_month_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles3',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('src', models.CharField(max_length=31)),
                ('text', models.TextField()),
                ('html', models.TextField()),
                ('img_src', models.CharField(max_length=31)),
                ('com_count', models.IntegerField()),
                ('month', models.CharField(default='1', max_length=15)),
            ],
        ),
    ]