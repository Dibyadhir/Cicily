# Generated by Django 4.1.3 on 2023-04-25 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Q_app', '0005_forgotpassword'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='forgotpassword',
            new_name='forgot_password',
        ),
    ]