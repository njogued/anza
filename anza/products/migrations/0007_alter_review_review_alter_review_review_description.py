# Generated by Django 4.2.10 on 2024-07-14 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_review_review_description_alter_review_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_description',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
