# Generated by Django 3.0.3 on 2020-03-18 13:37

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0003_remove_spotifyuser_extended_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifyuser',
            name='artist_count',
            field=jsonfield.fields.JSONField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='genre_count',
            field=jsonfield.fields.JSONField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='last_updated',
            field=models.DateField(default=None, null=True),
        ),
    ]
