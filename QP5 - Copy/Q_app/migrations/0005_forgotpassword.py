# Generated by Django 4.1.3 on 2023-04-24 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Q_app', '0004_rename_clientid_requirements_deptid'),
    ]

    operations = [
        migrations.CreateModel(
            name='forgotpassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=50)),
                ('confirm_password', models.CharField(max_length=50)),
            ],
        ),
    ]