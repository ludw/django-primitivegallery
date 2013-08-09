from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from primitivegallery.models import Image, Directory
from django.http import HttpResponse
from datetime import datetime, timedelta


def list(request, size='thumbnails', subfolder=''):
    pagesize = {'thumbnails': 150, 'small': 40, 'medium': 20}

    all_items = Directory(subfolder).list()
    p = Paginator(all_items, pagesize[size])

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    try:
        items = p.page(page)
    except (EmptyPage, InvalidPage):
        items = p.page(p.num_pages)

    breadcrumbs = []
    path = ''
    for segment in subfolder.split('/'):
        path += segment + '/'
        breadcrumbs.append({'name': segment, 'path': path})

    return render_to_response('primitivegallery/index.html', {
        'filelist': items,
        'size': size,
        'subfolder': subfolder,
        'breadcrumbs': breadcrumbs,
    })


def process_image(request):
    i = Image.objects.filter(status=0).order_by('-datestamp')
    if len(i) == 0:
        return HttpResponse("Nothing to process.")

    start = datetime.now()
    count = 0
    for image in i:
        if datetime.now() - start < timedelta(seconds=80):
            image.process()
            count += 1

    return render_to_response('primitivegallery/process.html', {
        'count': count
    })
