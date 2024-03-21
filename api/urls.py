from django.urls import path, include

# `book` uygulamasındaki views'ları import etmek için
from book.views import (
    SurahListCreateAPIView, SurahDetailAPIView,
    AuthorListCreateAPIView, AuthorDetailAPIView,
    VerseListCreateAPIView, VerseDetailAPIView,
    AudioListCreateAPIView, AudioDetailAPIView,
    TranslationListCreateAPIView, TranslationDetailAPIView,
    FootnoteListCreateAPIView, FootnoteDetailAPIView,
)

urlpatterns = [
    # Burada `book` app'ine ait views'ları doğrudan kullanıyoruz
    path('surahs/', SurahListCreateAPIView.as_view(), name='surah-list-create'),
    path('surahs/<int:pk>/', SurahDetailAPIView.as_view(), name='surah-detail'),
    path('authors/', AuthorListCreateAPIView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', AuthorDetailAPIView.as_view(), name='author-detail'),
    path('verses/', VerseListCreateAPIView.as_view(), name='verse-list-create'),
    path('verses/<int:pk>/', VerseDetailAPIView.as_view(), name='verse-detail'),
    path('audios/', AudioListCreateAPIView.as_view(), name='audio-list-create'),
    path('audios/<int:pk>/', AudioDetailAPIView.as_view(), name='audio-detail'),
    path('translations/', TranslationListCreateAPIView.as_view(), name='translation-list-create'),
    path('translations/<int:pk>/', TranslationDetailAPIView.as_view(), name='translation-detail'),
    path('footnotes/', FootnoteListCreateAPIView.as_view(), name='footnote-list-create'),
    path('footnotes/<int:pk>/', FootnoteDetailAPIView.as_view(), name='footnote-detail'),
]
