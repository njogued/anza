# Generated by Django 4.2.10 on 2024-06-24 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_business_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='categories',
        ),
        migrations.AddField(
            model_name='business',
            name='categories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='businesses', to='business.category'),
        ),
    ]
