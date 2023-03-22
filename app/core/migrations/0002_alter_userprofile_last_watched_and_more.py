# Generated by Django 4.0.8 on 2022-10-28 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='last_watched',
            field=models.ManyToManyField(blank=True, default=None, related_name='last_watched', to='core.movie'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='posts',
            field=models.ManyToManyField(blank=True, default=None, to='core.post'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='top_movies',
            field=models.ManyToManyField(blank=True, default=None, to='core.movie'),
        ),
    ]