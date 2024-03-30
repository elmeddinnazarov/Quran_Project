from django.core.management.base import BaseCommand
import requests
from book.models import RootChar

class Command(BaseCommand):
    help = 'API\'den RootChars verilerini çeker ve veritabanına kaydeder.'

    def handle(self, *args, **options):
        response = requests.get("https://api.acikkuran.com/rootchars")
        if response.status_code == 200:
            root_chars_data = response.json()['data']
            for item in root_chars_data:
                RootChar.objects.update_or_create(
                    id=item['id'],  # Bu kısmı id bazında güncelleme veya oluşturma için kullanıyoruz
                    defaults={
                        'latin': item.get('latin', ''),
                        'arabic': item.get('arabic', ''),
                        # 'root': Bu alan daha sonra doldurulacak
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"Toplam {len(root_chars_data)} RootChars veritabanına kaydedildi."))
        else:
            self.stdout.write(self.style.ERROR('RootChars verileri API\'den çekilemedi.'))
