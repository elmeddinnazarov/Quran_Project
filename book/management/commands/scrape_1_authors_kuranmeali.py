from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from book import models
from requests.exceptions import HTTPError, Timeout
import time


class Command(BaseCommand):


    def make_request_with_retry(self, url, max_retries=20, timeout=10):
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

    def handle(self, *args, **options):

        author_dict = {
            # "golpinarli": "Abdulbaki Gölpınarlı",
            # 'aakgul': "Abdullah-Ahmet Akgül",
            'aparliyan':"Abdullah Parlıyan",
            'ahmettekin': "Ahmet Tekin", 
            'ahmetvarol': "Ahmet Varol", 
            'alifikriyavuz': "Ali Fikri Yavuz",
            'bahaeddinsaglam': "Bahaeddin Sağlam", 
            'besimatalay': "Besim Atalay (1965)",
            'cemalkulunkoglu': "Cemal Külünkoğlu",
            'cemilsaid': "Cemil Said (1924)", 
            'diyanetislerieski': "Diyanet İşleri (Eski)",
            'kuranyolu': "Kur'an Yolu (Diyanet İşleri)",
            'diyanetvakfi': "Diyanet Vakfı", 
            'demiryent': "Emrah Demiryent", 
            'hayrat': "Hayrat Neşriyat", 
            'ilyasyorulmaz': "İlyas Yorulmaz", 
            'baltacioglu': "İsmayıl Hakkı Baltacıoğlu",
            'ismailhakkiizmirli': "İsmail Hakkı İzmirli",
            'ismailyakit': "İsmail Yakıt", 
            'kadricelik': "Kadri Çelik", 
            'mahmutkisa': "Mahmut Kısa",
            'mahmutozdemir': "Mahmut Özdemir",
            'mehmetcakir': "Mehmet Çakır",
            'mehmetcoban': "Mehmet Çoban", 
            'mehmetturk': "Mehmet Türk",
            'mustafacavdar': "Mustafa Çavdar", 
            'orhankuntman': "Orhan Kuntman",
            'osmanfirat': "Osman Fırat",
            'omernasuhi': "Ömer Nasuhi Bilmen",
            'suleymantevfik': "Süleyman Tevfik (1927)",
            'simsek': "Ümit Şimşek",
            'eskianadoluturkcesi': "Eski Anadolu Türkçesi",
            'satiralti': "Satır Altı (1534)",
            'bunyadov': "Z.Bünyadov - V.Məmmədəliyev"
        }
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
                url = f"https://kuranmeali.com/AyetKarsilastirma.php?sure={surah_number}&ayet={verse_number}"
                surah_details = self.get_surah_numbers_from_url(url)

                response = self.make_request_with_retry(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                mealler_div = soup.find('div', id='Mealler')
                for meal_div in mealler_div.find_all('div', recursive=False):
                    target = meal_div.get('id')
                    if target in author_dict:
                        author_full_name = author_dict[target]
                        author_div = meal_div.find('div', style=lambda value: value and 'width:150px;' in value, recursive=False)
                        verse_div = meal_div.find('div', style=lambda value: value and 'width:480px;' in value, recursive=False)
                        # author = self.save_author_full_name(author_div, author_full_name)
                        self.get_meal_details(verse_div, author_full_name, surah_details)
                    




    def save_author_full_name(self, author_data, author_full_name):
        author, create = models.Author.objects.get_or_create(full_name = author_full_name)
        return author





    def get_meal_details(self, translation_data, author_name, surah_details):
        target_translation = translation_data.find('span', style=lambda value: value and 'font-size:16px' in value)
        if target_translation:
            related_translation, translation_saved = self.save_related_translation(target_translation.text, surah_details, author_name)
            if translation_saved == True:
                a_tag = translation_data.find('a', href=lambda value: value and 'javascript:new_window(' in value)
                if a_tag:
                    href_value = a_tag['href']
                    start = href_value.find('"') + 1  
                    end = href_value.find('"', start) 
                    footnote_url = 'https://kuranmeali.com/' + href_value[start:end]
                    footnote, footnote_saved = self.get_meal_footnote(footnote_url, surah_details, related_translation)
                    self.stdout.write(self.style.SUCCESS(f'İlgili ayetin footnote bilgisi kaydedildi.'))
                else:
                    self.stdout.write(self.style.ERROR(f'İlgili ayete ait footnote bilgisi bulunamadı.'))
                self.stdout.write(self.style.SUCCESS(f'İlgili ayet başarılı bir şekilde kaydedildi.'))
            else:
                self.stdout.write(self.style.ERROR(f'İlgili ayet bilgisi kaydedilirken bir hata oluştu.'))
    

    def get_meal_footnote(self, footnote_url, surah_details, related_translation):
        print(footnote_url)
        response = self.make_request_with_retry(footnote_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        footnote_td = soup.find('td', style=lambda value: value and 'font: 16px EB Garamond;' in value)


        footnote, footnote_saved = self.save_related_footnote(footnote_td.text, surah_details, related_translation)
        return footnote, footnote_saved
    

    def save_related_footnote(self, footnote_data, surah_details, related_translation):
        footnote = ''
        if footnote_data is None:
            self.stdout.write(self.style.ERROR(f'FOOTNOTE HATA ---> {surah_details}'))
        else:
            print(footnote_data.strip())
            print(related_translation)
            return footnote, True


    def save_related_translation(self, translation_data, surah_details, author_name):
        translation = 'ilgili yazar'
        if translation_data is None:
            self.stdout.write(self.style.ERROR(f'TRANSLATION HATA ---> {surah_details} - {author_name}'))
        print(translation_data.strip())
        print(surah_details)
        print(author_name)
        return translation, True
    

    def get_surah_numbers_from_url(self, footnote_url):
        surah = footnote_url[-8] 
        verse = footnote_url[-1]
        surah_details = {surah:verse}
        return surah_details