# Generated by Django 4.0.8 on 2023-03-17 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='filmweb_nick',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]