from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

from .views import AlbumDetail, photos, download_zipped_album, download_all_zipped_albums

from django.conf.urls import include
from django.urls import path, include
from django.contrib import admin

#admin.autodiscover()

urlpatterns = [
    url(r'^photos$', photos, name='photos'),
    url(r'^photos/download/all$', download_all_zipped_albums, name='download_all_zipped_albums'),
    url(r'^photos/download/(?P<album_name>[-\w]+)/$', download_zipped_album, name='download_zipped_album'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/icons/favicon.ico', permanent=True)),
    url(r'^(?P<slug>[-\w]+)$', AlbumDetail.as_view(), name='album'),
    # Auth related urls
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout$', auth_views.logout, { 'next_page': '/', }, name='logout'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'views.handler404'




