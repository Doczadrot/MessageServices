from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.contrib import admin
from django.urls import path
from users.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('mailing/', include('mailing.urls', namespace='mailing')),
    path('', HomeView.as_view(), name='home'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
