# Generated by Django 4.1 on 2022-09-24 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_bio_user_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(default='profile_images/default.png', upload_to='profile_images'),
        ),
    ]
