# Generated by Django 4.2.4 on 2023-09-02 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0013_remove_articles3_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='app01.articles3'),
        ),
        migrations.DeleteModel(
            name='Articles2',
        ),
    ]
