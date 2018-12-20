#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import zipfile
import os
import io
import logging

from django.shortcuts import render
from django.http import HttpRequest
from django.http import Http404 
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from django.conf import settings

from wsgiref.util import FileWrapper

from .models import Album, AlbumImage
from lockdown.decorators import lockdown

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

@lockdown()
def photos(request):
    list = Album.objects.filter(is_visible=True).order_by('-created')
    paginator = Paginator(list, 10)
    logger.info("Albums list: {}".format(list))
    page = request.GET.get('page')
    logger.info(page)
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1) # If page is not an integer, deliver first page.
    except EmptyPage:
        albums = paginator.page(paginator.num_pages) # If page is out of range (e.g.  9999), deliver last page of results.

    return render(request, 'photos.html', { 'albums': list })


class AlbumDetail(DetailView):
     model = Album

     def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['images'] = AlbumImage.objects.filter(album=self.object.id)
        return context



def download_zipped_album(request, album_name):
    album = Album.objects.filter(slug=album_name).order_by('-created')
    if album is None:
        logger.error("Album {} does not exist!".format(album_name))
        raise Http404 
    # album_name = request.GET.get('album_name')
    logger.info("album_name: %s"%album_name)
    zip_file_name = album_name+'.zip'

    images = AlbumImage.objects.filter(album=album[0].id)
    logger.info("images: {}".format(images))
    

    files = []
    for img in images:
        files.append((img.alt, os.path.join(settings.MEDIA_URL, os.path.join(AlbumImage._meta.get_field('image').upload_to, img.alt))))
    # create binary buffer 
    album_buffer = io.BytesIO()
    with zipfile.ZipFile(album_buffer, 'w', zipfile.ZIP_DEFLATED) as zip:
        for name, f in files:
            logger.info(img.alt)
            zip.write(f, name)
    # flush the buffer
    album_buffer.flush()

    # apply the buffer raw value to the response
    response = HttpResponse(album_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s' % zip_file_name

    # close the buffer
    album_buffer.close()
    return response



def download_all_zipped_albums(request):
    albums = Album.objects.filter(is_visible=True).order_by('-created')
    if albums is None:
        logger.error("No albums in database!")
        raise Http404 

    final_zip_file_name = "JustynaLukaszWeddingPhotos.zip"

    # create binary buffer for all the buffers 
    albums_buffer = io.BytesIO()
    with zipfile.ZipFile(albums_buffer, 'w', zipfile.ZIP_DEFLATED) as zip:
        # zip all files at once
        for album in albums:
            # read all the images of the album
            images = AlbumImage.objects.filter(album=album.id)
            album_name = album.slug
            logger.info("album_name: %s"%album_name)
            logger.info("images: {}".format(images))

            files = []
            for img in images:
                files.append((img.alt, os.path.join(settings.MEDIA_URL, os.path.join(AlbumImage._meta.get_field('image').upload_to, img.alt))))
            # save binary data 
            for name, f in files:
                logger.warning(name)
                zip.write(f, name)

    # flush the buffer
    albums_buffer.flush()

    # apply the buffer raw value to the response
    response = HttpResponse(albums_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s' % final_zip_file_name

    # close the albums buffer
    albums_buffer.close() 
    return response



def handler404(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'handler404.html', None, None, 404)