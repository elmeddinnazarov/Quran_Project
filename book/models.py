from django.db import models

# Create your models here.


class Surah(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()
    name_means = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    number = models.IntegerField()
    verse = models.ForeignKey("book.Verse", verbose_name="s_verse", on_delete=models.CASCADE)
    audio = models.ForeignKey("book.Audio", verbose_name="s_audio", on_delete=models.CASCADE)
    verse_count = models.IntegerField()

    def __str__(self):
        return self.name
    

class Author(models.Model):
    full_name = models.CharField(max_length=50)
    bio = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50)
    image = models.ImageField(upload_to=None)

    def __str__(self):
        return self.full_name
    

class Verse(models.Model):
    number = models.IntegerField()
    transcription = models.TextField()
    translation = models.ForeignKey("book.Translation", verbose_name="v_translation", on_delete=models.CASCADE)

    def __str__(self):
        return self.number
    

class Audio(models.Model):
    mp3 = models.URLField(max_length=200)
    duration = models.DurationField()

    def __str__(self):
        return self.id
    

class Translation(models.Model):
    text = models.TextField()
    footnote = models.ForeignKey("book.Footnote", verbose_name="t_footnote", on_delete=models.CASCADE)

    def __str__(self):
        return self.id
    

class Footnote(models.Model):
    number = models.IntegerField()
    text =models.TextField()

    def __str__(self):
        return self.number