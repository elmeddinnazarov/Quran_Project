from django.core.management.base import BaseCommand
import requests
from book.models import Author, Translation, Verse, Footnote
from requests.exceptions import HTTPError, Timeout
import time
class Command(BaseCommand):
    help = 'API\'den yazar bilgilerini çeker ve veritabanına kaydeder'


    def handle(self, *args, **options):
        surah_numbers = {
            1: 7, 2: 286, 3: 200, 4: 176, 5: 120, 6: 165, 7: 206, 8: 75, 9: 129, 10: 109,
            11: 123, 12: 111, 13: 43, 14: 52, 15: 99, 16: 128, 17: 111, 18: 110, 19: 98, 20: 135,
            21: 112, 22: 78, 23: 118, 24: 64, 25: 77, 26: 227, 27: 93, 28: 88, 29: 69, 30: 60,
            31: 34, 32: 30, 33: 73, 34: 54, 35: 45, 36: 83, 37: 182, 38: 88, 39: 75, 40: 85,
            41: 54, 42: 53, 43: 89, 44: 59, 45: 37, 46: 35, 47: 38, 48: 29, 49: 18, 50: 45,
            51: 60, 52: 49, 53: 62, 54: 55, 55: 78, 56: 96, 57: 29, 58: 22, 59: 24, 60: 13,
            61: 14, 62: 11, 63: 11, 64: 18, 65: 12, 66: 12, 67: 30, 68: 52, 69: 52, 70: 44,
            71: 28, 72: 28, 73: 20, 74: 56, 75: 40, 76: 31, 77: 50, 78: 40, 79: 46, 80: 42,
            81: 29, 82: 19, 83: 36, 84: 25, 85: 22, 86: 17, 87: 19, 88: 26, 89: 30, 90: 20,
            91: 15, 92: 21, 93: 11, 94: 8, 95: 8, 96: 19, 97: 5, 98: 8, 99: 8, 100: 11,
            101: 11, 102: 8, 103: 3, 104: 9, 105: 5, 106: 4, 107: 7, 108: 3, 109: 6, 110: 3,
            111: 5, 112: 4, 113: 5, 114: 6
            }
        for surah_number, verse_count in surah_numbers.items():
            for verse_number in range(1, verse_count+1):
                url = f'https://api.acikkuran.com/surah/{surah_number}/verse/{verse_number}/translations'
                response = self.make_request_with_retry(url)
                data = response.json()['data']  # API'den gelen yanıt
                for translation_data in data:
                    if translation_data['text'] is not None:
                        related_verse = Verse.objects.filter(verse_number = verse_number, related_surah__surah_number=surah_number).first()
                        target_author_name = translation_data['author']['name']
                        related_author = Author.objects.filter(full_name = target_author_name).first()

                        trans, create = Translation.objects.get_or_create(
                            text = translation_data['text'],
                            author = related_author,
                            verse = related_verse
                        )
                        self.stdout.write(self.style.SUCCESS(f'Translation verisi kaydedildi. --> Surah:{surah_number}, Verse:{verse_number}'))
                        self.fetch_footnotes(translation_data, trans)
                    else:
                        self.stdout.write(self.style.ERROR(f'Translation verisi bulunamadı.'))





    def fetch_footnotes(self, data, trans):
        if data['footnotes'] is not None:
            for footnote in data['footnotes']:
                note, create = Footnote.objects.get_or_create(
                    text=footnote['text'],
                    number = footnote['number'],
                    translation = trans
                )
            self.stdout.write(self.style.SUCCESS(f'Footnote verileri kaydedildi.'))
        else:
            self.stdout.write(self.style.ERROR(f'ilgili tercüme için footnote verisi bulunamadı.'))



    def make_request_with_retry(self, url, max_retries=5, timeout=10):
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