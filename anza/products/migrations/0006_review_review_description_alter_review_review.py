# Generated by Django 4.2.10 on 2024-07-14 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_productimage_is_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(default=''),
        ),
    ]
