# Generated by Django 4.0.8 on 2022-10-22 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_filmweb_nick'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='timestamp',
            field=models.DateField(auto_now_add=True),
        ),
    ]
