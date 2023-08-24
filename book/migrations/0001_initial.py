# Generated by Django 4.2.4 on 2023-08-24 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mp3', models.URLField()),
                ('duration', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('bio', models.TextField(blank=True, null=True)),
                ('language', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to=None)),
            ],
        ),
        migrations.CreateModel(
            name='Footnote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('footnote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.footnote', verbose_name='t_footnote')),
            ],
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('transcription', models.TextField()),
                ('translation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.translation', verbose_name='v_translation')),
            ],
        ),
        migrations.CreateModel(
            name='Surah',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('slug', models.SlugField()),
                ('name_means', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('number', models.IntegerField()),
                ('verse_count', models.IntegerField()),
                ('audio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.audio', verbose_name='s_audio')),
                ('verse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.verse', verbose_name='s_verse')),
            ],
        ),
    ]