from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Surah)
admin.site.register(models.Author)
admin.site.register(models.Footnote)
admin.site.register(models.VerseZero)
admin.site.register(models.Word)
admin.site.register(models.Root)
admin.site.register(models.RootChar)
admin.site.register(models.Differential)

class TranslationAdmin(admin.ModelAdmin):
    list_display = ('get_surah', 'get_verse_number', 'author')
    ordering = ('verse__related_surah__surah_number', 'verse__verse_number', 'author__full_name')

    def get_surah(self, obj):
        return obj.verse.related_surah.name
    get_surah.admin_order_field = 'verse__related_surah__surah_number'  # Sıralama için alan belirtir

    def get_verse_number(self, obj):
        return obj.verse.verse_number
    get_verse_number.admin_order_field = 'verse__verse_number'  # Sıralama için alan belirtir
    get_verse_number.short_description = 'Verse Number'  # Kolon başlığı

admin.site.register(models.Translation, TranslationAdmin)



class VerseAdmin(admin.ModelAdmin):
    list_display = ('related_surah', 'verse_number')
    ordering = ('related_surah__surah_number', 'verse_number')

admin.site.register(models.Verse, VerseAdmin)



class AudioAdmin(admin.ModelAdmin):
    list_display = ['related_surah', 'language']
    
    def get_queryset(self, request):
        # 'related_surah__surah_number' kullanarak sıralama yap
        queryset = super().get_queryset(request).order_by('related_surah__surah_number', 'language')
        return queryset

admin.site.register(models.Audio, AudioAdmin)