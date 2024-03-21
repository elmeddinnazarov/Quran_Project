# Generated by Django 4.2.4 on 2024-03-20 23:48

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
                ('mp3', models.URLField(blank=True, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=20, null=True)),
                ('voiced_by', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('bio', models.TextField(blank=True, null=True)),
                ('source', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('language', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to=None)),
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
                ('text', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.author', verbose_name='t_author')),
                ('footnote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.footnote', verbose_name='t_footnote')),
            ],
        ),
        migrations.CreateModel(
            name='VerseZero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verse_number', models.IntegerField()),
                ('verse', models.TextField()),
                ('verse_simplified', models.TextField(blank=True, null=True)),
                ('verse_without_vowel', models.TextField(blank=True, null=True)),
                ('transcription', models.TextField(blank=True, null=True)),
                ('transcription_en', models.TextField(blank=True, null=True)),
                ('page_number', models.IntegerField()),
                ('juz_number', models.IntegerField()),
                ('translation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.translation', verbose_name='v_translation')),
            ],
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verse_number', models.IntegerField()),
                ('verse', models.TextField()),
                ('verse_simplified', models.TextField(blank=True, null=True)),
                ('verse_without_vowel', models.TextField(blank=True, null=True)),
                ('transcription', models.TextField(blank=True, null=True)),
                ('transcription_en', models.TextField(blank=True, null=True)),
                ('page_number', models.IntegerField()),
                ('juz_number', models.IntegerField()),
                ('translation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.translation', verbose_name='v_translation')),
            ],
        ),
        migrations.CreateModel(
            name='Surah',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('name_en', models.CharField(blank=True, max_length=20, null=True)),
                ('name_arabic', models.CharField(blank=True, max_length=50, null=True)),
                ('name_means', models.CharField(blank=True, max_length=20, null=True)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, null=True)),
                ('number', models.IntegerField()),
                ('verse_count', models.IntegerField()),
                ('page_number', models.IntegerField()),
                ('audio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.audio', verbose_name='s_audio')),
                ('verse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.verse', verbose_name='s_verse')),
                ('zero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.versezero', verbose_name='s_zero_verse')),
            ],
        ),
    ]
