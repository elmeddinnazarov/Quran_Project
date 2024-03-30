from rest_framework import serializers
from .models import Surah, Author, Verse, Audio, Translation, Footnote, VerseZero, Word

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'

class VerseZeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerseZero
        fields = '__all__'

class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = '__all__'



class SurahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surah
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = '__all__'

class FootnoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footnote
        fields = '__all__'



