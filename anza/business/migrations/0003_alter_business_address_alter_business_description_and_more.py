# Generated by Django 4.2.10 on 2024-08-11 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='description',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='business',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]