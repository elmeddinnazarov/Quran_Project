from django.db import models

# Create your models here.


class Surah(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    name_en = models.CharField(max_length=20, blank=True, null=True)
    name_original = models.CharField(max_length=50, blank=True, null=True)
    name_translation_tr = models.CharField(max_length=30, blank=True, null=True)
    name_translation_en = models.CharField(max_length=30, blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    surah_number = models.IntegerField()
    verse_count = models.IntegerField()
    page_number = models.IntegerField()
    zero = models.ForeignKey("book.VerseZero", verbose_name="zero_verse", on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['surah_number']

class Audio(models.Model):
    mp3 = models.URLField(max_length=200, blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True)
    voiced_by = models.CharField(max_length=50, blank=True, null=True)
    related_surah = models.ForeignKey("book.Surah", verbose_name="surah", on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)


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
    related_surah = models.ForeignKey("book.Surah", verbose_name="surah", on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    verse_word = models.ManyToManyField("book.Word", verbose_name="words")

    def __str__(self):
        return f"""{self.related_surah.name} - {str(self.verse_number)}"""
    
    
class VerseZero(models.Model):
    verse_number = models.IntegerField()
    verse = models.TextField()
    verse_simplified = models.TextField(blank=True, null=True)
    verse_without_vowel = models.TextField(blank=True, null=True)
    transcription = models.TextField(blank=True, null=True)
    transcription_en = models.TextField(blank=True, null=True)
    page_number = models.IntegerField()
    juz_number = models.IntegerField()
    verse_word = models.ManyToManyField("book.Word", verbose_name="words")

    def __str__(self):
        return 'Verse Zero'

    

class Translation(models.Model):
    text = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Author, verbose_name="author", on_delete=models.SET_DEFAULT, default=None, blank=True, null=True) 
    verse = models.ForeignKey(Verse, on_delete=models.SET_DEFAULT, default=None, related_name='translation')

    def __str__(self):
        return f"{str(self.verse.related_surah.name)} - {str(self.verse.verse_number)} - {self.author.full_name}"
    

class Footnote(models.Model):
    number = models.IntegerField(blank=True, null=True)
    text =models.TextField(blank=True, null=True)
    translation = models.ForeignKey(Translation, verbose_name="translation", on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)


    def __str__(self):
        return f"{self.translation.author.full_name} - Surah:{self.translation.verse.related_surah.name} - Verse:{self.translation.verse.verse_number} - Footnote:{str(self.number)}"



class Word(models.Model):
    sort_number = models.IntegerField(blank=True, null=True)
    transcription_tr = models.CharField(max_length=100, blank=True, null=True)
    arabic = models.CharField(max_length=100, blank=True, null=True)
    translation_tr = models.CharField(max_length=100, blank=True, null=True)
    translation_en = models.CharField(max_length=100, blank=True, null=True) #
    transcription_en = models.CharField(max_length=100, blank=True, null=True) #
    prop_1 = models.CharField(max_length=100, blank=True, null=True)
    prop_2 = models.CharField(max_length=100, blank=True, null=True)
    prop_3 = models.CharField(max_length=100, blank=True, null=True)
    prop_4 = models.CharField(max_length=100, blank=True, null=True)
    prop_5 = models.CharField(max_length=100, blank=True, null=True)
    prop_6 = models.CharField(max_length=100, blank=True, null=True)
    prop_7 = models.CharField(max_length=100, blank=True, null=True)
    prop_8 = models.CharField(max_length=100, blank=True, null=True)
    root = models.ForeignKey("book.Root", verbose_name="root", on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.transcription_tr} - {str(self.arabic)}"



class Root(models.Model):
    latin = models.CharField(max_length=20, blank=True, null=True)
    arabic = models.CharField(max_length=30, blank=True, null=True)
    transcription = models.CharField(max_length=50, blank=True, null=True)
    transcription_en = models.CharField(max_length=50, blank=True, null=True)
    mean = models.TextField(blank=True, null=True)
    mean_en = models.TextField(blank=True, null=True)
    char = models.ForeignKey("book.RootChar", verbose_name="character", on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)



    def __str__(self):
        return f"{self.latin} - {self.transcription}"

class Differential(models.Model):
    diff = models.CharField(max_length=50, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    root = models.ForeignKey("book.Root", verbose_name="diffs", on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.diff} - {self.count}"
    

class RootChar(models.Model):
    latin = models.CharField(max_length=5, blank=True, null=True)
    arabic = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.latin} - {str(self.arabic)}"






