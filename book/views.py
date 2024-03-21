from rest_framework import generics
from .models import Surah, Author, Verse, Audio, Translation, Footnote
from .serializers import SurahSerializer, AuthorSerializer, VerseSerializer, AudioSerializer, TranslationSerializer, FootnoteSerializer

class SurahListCreateAPIView(generics.ListCreateAPIView):
    queryset = Surah.objects.all()
    serializer_class = SurahSerializer

class SurahDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Surah.objects.all()
    serializer_class = SurahSerializer

class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class VerseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Verse.objects.all()
    serializer_class = VerseSerializer

class VerseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Verse.objects.all()
    serializer_class = VerseSerializer

class AudioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

class AudioDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

class TranslationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer

class TranslationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer

class FootnoteListCreateAPIView(generics.ListCreateAPIView):
    queryset = Footnote.objects.all()
    serializer_class = FootnoteSerializer

class FootnoteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Footnote.objects.all()
    serializer_class = FootnoteSerializer
