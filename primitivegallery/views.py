from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from primitivegallery.models import Image, Directory
from django.http import HttpResponse, Http404
from datetime import timedelta
from django.utils import timezone


def list(request, size='thumbnails', subfolder=''):
    pagesize = {'thumbnails': 250, 'small': 100, 'medium': 50}

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


def slideshow(request, subfolder=''):
    index = 0
    try:
        startid = int(request.GET.get('start'))
        items = Image.objects.filter(path__startswith=subfolder, status__gt=0).order_by('datetaken')
        for i, item in enumerate(items):
            if item.pk == startid:
                index = i
    except:
        pass
    return render_to_response('primitivegallery/slideshow.html', {
        'subfolder': subfolder,
        'index': index,
    })


def process_image(request):
    i = Image.objects.filter(status=0).order_by('-datestamp')
    if len(i) == 0:
        return HttpResponse("Nothing to process.")

    start = timezone.now()
    count = 0
    for image in i:
        if timezone.now() - start < timedelta(seconds=80):
            image.process()
            count += 1

    return render_to_response('primitivegallery/process.html', {
        'count': count
    })


def api_list(request, size='thumbnails', subfolder=''):
    try:
        index = int(request.GET.get('index'))
    except:
        index = 0

    try:
        items = Image.objects.filter(path__startswith=subfolder, status__gt=0).order_by('datetaken')[max(index - 2, 0):index + 3]
        item = Image.objects.filter(path__startswith=subfolder, status__gt=0).order_by('datetaken')[index]
    except IndexError:
        raise Http404

    return render_to_response('primitivegallery/api_list.json', {
        'items': items,
        'item': item,
    }, content_type='application/json')
