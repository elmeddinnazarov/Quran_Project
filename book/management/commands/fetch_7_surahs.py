from django.core.management.base import BaseCommand
import requests
from book.models import Surah, VerseZero

class Command(BaseCommand):
    help = 'Açık Kuran API\'den her bir Surah için detaylı bilgileri çeker ve veritabanına kaydeder'

    def handle(self, *args, **options):
        # Veritabanındaki ilk VerseZero nesnesini al
        verse_zero = VerseZero.objects.first()

        for surah_id in range(1, 115):  # Toplam 114 sure olduğu için
            response = requests.get(f"https://api.acikkuran.com/surah/{surah_id}")
            if response.status_code == 200:
                surah_data = response.json()['data']
                surah, created = Surah.objects.get_or_create(
                    name=surah_data['name'],
                    id = surah_data.get('id'),
                    surah_number =  surah_data['id'],

                    defaults={
                        'name_en': surah_data.get('name_en'),
                        'name_original': surah_data.get('name_original'),
                        'name_translation_tr': surah_data.get('name_translation_tr', ''),
                        'name_translation_en': surah_data.get('name_translation_en', ''),
                        'slug': surah_data.get('slug'),
                        'description': '',  # API'den açıklama bilgisi yoksa varsayılan bir değer
                        'verse_count': surah_data['verse_count'],
                        'page_number': surah_data['page_number'],
                        'zero': verse_zero
                    }
                )

            

                self.stdout.write(self.style.SUCCESS(f'Surah "{surah.name}" detayları başarıyla güncellendi.'))
            else:
                self.stdout.write(self.style.ERROR(f'Surah ID {surah_id} için bilgiler çekilemedi.'))
