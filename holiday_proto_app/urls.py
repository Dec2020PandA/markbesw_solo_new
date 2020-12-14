
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('create_user', views.register),
    path('login', views.login),
    path('success', views.success),
    path('sendmail', views.sendmail),
    path('upload', views.upload),
    path('update_text/<int:card_id>', views.update_text),
    path('update_image/<int:card_id>', views.update_image),
    path('make_card', views.make_card)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
