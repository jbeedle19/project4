# Generated by Django 4.0.3 on 2022-03-18 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_following_post_like'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
    ]
