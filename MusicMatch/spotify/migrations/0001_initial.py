# Generated by Django 3.0.3 on 2020-02-15 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('artists', models.ManyToManyField(to='spotify.Artist')),
            ],
        ),
        migrations.AddField(
            model_name='artist',
            name='genres',
            field=models.ManyToManyField(to='spotify.Genre'),
        ),
    ]