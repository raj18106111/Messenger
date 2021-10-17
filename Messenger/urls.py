from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('chatapp.urls')),
    path('accounts/',include('accounts.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
