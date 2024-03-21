from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Surah)
admin.site.register(models.Verse)
admin.site.register(models.Translation)
admin.site.register(models.Author)
admin.site.register(models.Footnote)
admin.site.register(models.Audio)
admin.site.register(models.VerseZero)