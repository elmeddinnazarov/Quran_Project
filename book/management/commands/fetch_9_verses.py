from django.core.management.base import BaseCommand
import requests
from book.models import Surah, Verse
from requests.exceptions import HTTPError, Timeout
import time
class Command(BaseCommand):
    help = 'Açık Kuran API\'den her bir Surah için Ayet bilgilerini çeker'

    def handle(self, *args, **options):
        surahs = Surah.objects.all()
        for surah in surahs:
            # 'surah.id' yerine 'surah.surah_number' kullanılıyor
            for verse_number in range(1, surah.verse_count + 1):
                url = f"https://api.acikkuran.com/surah/{surah.surah_number}/verse/{verse_number}"
                response = self.make_request_with_retry(url)
                if response.status_code == 200:
                    verse_data = response.json()['data']
                    Verse.objects.update_or_create(
                        related_surah=surah,  # Surah ile ilişkilendirme
                        verse_number=verse_number,
                        defaults={
                            'verse': verse_data.get('verse'),
                            'verse_simplified': verse_data.get('verse_simplified', ''),
                            'verse_without_vowel': verse_data.get('verse_without_vowel', ''),
                            'transcription': verse_data.get('transcription', ''),
                            'transcription_en': verse_data.get('transcription_en', ''),
                            'page_number': verse_data.get('page'),
                            'juz_number': verse_data.get('juz_number'),
                        }
                    )
                    self.stdout.write(self.style.SUCCESS(f'Verse {verse_number} of Surah {surah.name} was successfully updated.'))
                else:
                    self.stdout.write(self.style.ERROR(f'Failed to fetch Verse {verse_number} for Surah {surah.name}. URL: {url}'))



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