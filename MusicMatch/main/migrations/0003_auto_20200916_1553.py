# Generated by Django 3.0.7 on 2020-09-20 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200909_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='artists',
        ),
        migrations.RemoveField(
            model_name='spotifyuser',
            name='artist_count',
        ),
        migrations.RemoveField(
            model_name='spotifyuser',
            name='genre_count',
        ),
        migrations.RemoveField(
            model_name='spotifyuser',
            name='songs',
        ),
        migrations.DeleteModel(
            name='Artist',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='Song',
        ),
        migrations.RemoveField(
            model_name='extendeduser',
            name='spotify_account',
        ),
        migrations.DeleteModel(
            name='SpotifyUser',
        ),
        migrations.AddField(
            model_name='extendeduser',
            name='spotify_account',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
