# Generated by Django 4.2.10 on 2024-07-14 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_upvote_upvote_unique_review_user_upvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='is_cover',
            field=models.BooleanField(default=False),
        ),
    ]
