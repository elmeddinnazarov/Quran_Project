from django.urls import path, include

app_name = "book"


urlpatterns = [
    # Diğer URL yapılandırmaları
    path('api/', include('api.urls')),  # `api` app'ine yönlendirme
]