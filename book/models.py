from django.db import models

# Create your models here.


class Surah(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    name_en = models.CharField(max_length=20, blank=True, null=True)
    name_arabic = models.CharField(max_length=50, blank=True, null=True)
    name_means = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    number = models.IntegerField()
    verse_count = models.IntegerField()
    page_number = models.IntegerField()
    zero = models.ForeignKey("book.VerseZero", verbose_name="s_zero_verse", on_delete=models.CASCADE)
    verse = models.ForeignKey("book.Verse", verbose_name="s_verse", on_delete=models.CASCADE)
    audio = models.ForeignKey("book.Audio", verbose_name="s_audio", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Author(models.Model):
    full_name = models.CharField(max_length=50)
    bio = models.TextField(blank=True, null=True)
    source = models.URLField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50)
    image = models.ImageField(upload_to=None, blank=True, null=True)

    def __str__(self):
        return self.full_name
    

class Verse(models.Model):
    verse_number = models.IntegerField()
    verse = models.TextField()
    verse_simplified = models.TextField(blank=True, null=True)
    verse_without_vowel = models.TextField(blank=True, null=True)
    transcription = models.TextField(blank=True, null=True)
    transcription_en = models.TextField(blank=True, null=True)
    page_number = models.IntegerField()
    juz_number = models.IntegerField()
    translation = models.ForeignKey("book.Translation", verbose_name="v_translation", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.verse_number)
    
class VerseZero(models.Model):
    verse_number = models.IntegerField()
    verse = models.TextField()
    verse_simplified = models.TextField(blank=True, null=True)
    verse_without_vowel = models.TextField(blank=True, null=True)
    transcription = models.TextField(blank=True, null=True)
    transcription_en = models.TextField(blank=True, null=True)
    page_number = models.IntegerField()
    juz_number = models.IntegerField()
    translation = models.ForeignKey("book.Translation", verbose_name="v_translation", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.verse_number)

class Audio(models.Model):
    mp3 = models.URLField(max_length=200, blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True)
    voiced_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.id)
    

class Translation(models.Model):
    text = models.TextField(blank=True, null=True)
    footnote = models.ForeignKey("book.Footnote", verbose_name="t_footnote", on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey("book.Author", verbose_name="t_author", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    

class Footnote(models.Model):
    number = models.IntegerField(blank=True, null=True)
    text =models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.number)