# Generated by Django 4.2.3 on 2024-05-21 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='msgfromadmin',
            name='logo',
            field=models.ImageField(default='avatar.png', upload_to='Logos'),
        ),
    ]
