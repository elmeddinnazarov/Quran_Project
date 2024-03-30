from django.core.management.base import BaseCommand
import requests
from datetime import timedelta
from book.models import Surah, Audio

class Command(BaseCommand):
    help = 'Fetches and updates separate audio data for each existing Surah in both English and Arabic.'

    def handle(self, *args, **options):
        surahs = Surah.objects.all()

        for surah in surahs:
            response = requests.get(f"https://api.acikkuran.com/surah/{surah.surah_number}")
            if response.status_code == 200:
                audio_data = response.json()["data"]["audio"]
                
                # Türkçe audio için Audio modeline kaydet
                Audio.objects.update_or_create(
                    related_surah=surah,
                    language="tr",  # Türkçe ses dosyası için 'tr' dil kodunu kullanıyoruz.
                    defaults={
                        'mp3': audio_data["mp3"],
                        'duration': timedelta(seconds=audio_data["duration"]),
                        'voiced_by': '',  # Eğer seslendiren kişi bilgisi mevcutsa buraya ekleyebilirsiniz.
                    }
                )

                # İngilizce audio için Audio modeline kaydet
                Audio.objects.update_or_create(
                    related_surah=surah,
                    language="en",  # İngilizce ses dosyası için 'en' dil kodunu kullanıyoruz.
                    defaults={
                        'mp3': audio_data["mp3_en"],
                        'duration': timedelta(seconds=audio_data["duration_en"]),
                        'voiced_by': '',  # Eğer seslendiren kişi bilgisi mevcutsa buraya ekleyebilirsiniz.
                    }
                )

                self.stdout.write(self.style.SUCCESS(f"Audio for Surah {surah.name} ({surah.surah_number}) in both English and Arabic updated successfully."))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to fetch audio for Surah {surah.name} ({surah.surah_number})."))
