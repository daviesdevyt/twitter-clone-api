# Generated by Django 4.1 on 2022-08-08 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_profile_username_alter_profile_profilepic'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
