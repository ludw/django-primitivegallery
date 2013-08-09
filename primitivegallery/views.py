from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from primitivegallery.models import Image, Directory
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from datetime import datetime, timedelta
from primitivegallery.forms import UploadFileForm


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


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            process_files(request.FILES.getlist('files'), request.POST.get('directory'))
            return HttpResponseRedirect(reverse('imagegrid.views.upload'))
    else:
        form = UploadFileForm()

    return render_to_response('primitivegallery/upload.html', {
        'form': form
    }, context_instance=RequestContext(request))


def process_files(files, path):
    print path
    for f in files:
        print f
        #with open('some/file/name.txt', 'wb+') as destination:
        #    for chunk in f.chunks():
        #        destination.write(chunk)
