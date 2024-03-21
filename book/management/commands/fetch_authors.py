from django.core.management.base import BaseCommand
import requests
from book.models import Author

class Command(BaseCommand):
    help = 'API\'den yazar bilgilerini çeker ve veritabanına kaydeder'

    def handle(self, *args, **options):
        url = 'https://api.acikkuran.com/authors'
        response = requests.get(url)
        data = response.json()  # API'den gelen yanıt

        # 'data' anahtarının altındaki listeyi döngüye al
        for author in data['data']:
            # Veritabanına yazar bilgilerini kaydet
            Author.objects.create(
                description=author['description'],
                language=author['language'],
                full_name=author['name'],
                source=author['url']
            )

        self.stdout.write(self.style.SUCCESS(f'Toplam {len(data["data"])} yazar veritabanına kaydedildi.'))
