from django.core.management.base import BaseCommand
import requests
from book.models import VerseZero
from requests.exceptions import HTTPError, Timeout
import time

class Command(BaseCommand):
    help = 'API\'den yazar bilgilerini çeker ve veritabanına kaydeder'

    def handle(self, *args, **options):
        # Yazarların idlerinden oluşan  liste oluştur
        authors_ids = []
        url = "https://api.acikkuran.com/authors"
        response = self.make_request_with_retry(url)
        data = response.json()['data']
        for authors_data in data:
            authors_ids.append(authors_data['id'])
        
        
        for author_id in authors_ids:
            url = f'https://api.acikkuran.com/surah/1/verse/1?author={author_id}'
            response = self.make_request_with_retry(url)
            data = response.json()['data']
            zero, create = VerseZero.objects.get_or_create(
                verse_number = 0,
                verse = data['verse'],
                defaults={
                    'verse_simplified': data['verse_simplified'],
                    'verse_without_vowel': data['verse_without_vowel'],
                    'transcription': data['transcription'],
                    'transcription_en': data['transcription_en'],
                    'page_number': data['page'],
                    'juz_number': data['juz_number']
                }
            )


    def make_request_with_retry(self, url, max_retries=10, timeout=5):
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(url, timeout=timeout)
                # Hata kodlarına bak
                response.raise_for_status()
                return response  # İstek başarılı olursa, yanıtı döndür
            except HTTPError as http_err:
                if response.status_code == 429:
                    # Rate limit hatası için bekleme süresi
                    retry_after = int(response.headers.get('Retry-After', 1))
                    print(f'Rate limit aşıldı, {retry_after} saniye sonra tekrar denenecek.')
                    time.sleep(retry_after)
                else:
                    print(f'HTTP error occurred: {http_err}')
                    break  # Diğer HTTP hatalarında döngüden çık
            except Timeout:
                print(f'Request timed out, retrying... ({retries + 1}/{max_retries})')
                time.sleep(1)  # Zaman aşımı durumunda beklet
            except Exception as err:
                print(f'Other error occurred: {err}')
                break  # Beklenmedik bir hata oluştuğunda döngüden çık
            retries += 1

        print(f'Maximum retry limit reached ({max_retries}). Request failed.')
        return None