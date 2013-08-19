import os
import subprocess
from datetime import datetime
from django.conf import settings
from django.db import models
from os.path import basename, dirname, exists, isfile, join
from PIL.ExifTags import TAGS
from PIL.Image import open
from django.utils import timezone


class Image(models.Model):
    path = models.CharField(max_length=500, unique=True)
    datestamp = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
    datetaken = models.DateTimeField(null=True)

    def name(self, size=None):
        if size:
            return '.' + size + '_' + basename(self.path)
        return basename(self.path)

    def dir(self):
        return dirname(self.path)

    def url(self, size=''):
        file = self.name(size)
        path = join(settings.PRIMITIVE_GALLERY['IMAGE_URL'], self.dir(), file)
        if exists(self.local(size)):
            return path
        if self.status != 0:
            self.status = 0
            self.save()
        if not exists(self.local()):
            print self.path
            self.delete()
        return join(settings.STATIC_URL, 'primitivegallery/img/placeholder_' + size + '.png')

    def local(self, size=''):
        file = self.name(size)
        return join(settings.PRIMITIVE_GALLERY['IMAGE_ROOT'], self.dir(), file)

    def process(self):
        if self.status > 0:
            return

        filepath = self.local()
        mediumpath = self.local('medium')
        smallpath = self.local('small')
        thumbpath = self.local('thumb')

        self.status = 1

        self._autorot(filepath)

        if not exists(mediumpath):
            retcode = self._create_resized(filepath, mediumpath, '900x600')
            if retcode > 0:
                self.status = 2

        if not exists(smallpath):
            retcode = self._create_resized(mediumpath, smallpath, '480x320')
            if retcode > 0:
                self.status = 2

        if not exists(thumbpath):
            retcode = self._create_thumbnail(smallpath, thumbpath, '100x100')
            if retcode > 0:
                self.status = 2

        try:
            self.datetaken = self.exiftaken()
        except IOError:
            pass
        self.save()

    def _autorot(self, infile):
        return subprocess.call(["jhead", '-autorot', infile])

    def _create_thumbnail(self, infile, outfile, size):
        return subprocess.call([
            'convert', infile,
            '-thumbnail', size + '^',
            '-gravity', 'center',
            '-extent', size,
            outfile
        ])

    def _create_resized(self, infile, outfile, size):
        return subprocess.call([
            'convert', infile,
            '-resize', size,
            '-unsharp', '1.0x1.0+0.5+0.10',
            outfile
        ])

    def taken(self):
        if self.datetaken:
            return self.datetaken
        return timezone.now()

    def exiftaken(self):
        i = open(self.local())
        info = i._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == 'DateTimeOriginal':
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        return timezone.now()

    def __unicode__(self):
        return self.path


class Directory:

    def __init__(self, subfolder):
        self.subfolder = subfolder

    def get_image(self, localpath, path):
        contained_files = os.listdir(localpath)
        for c_file in contained_files:
            c_localpath = join(localpath, c_file)
            c_path = join(path, c_file)
            if c_file[0] != '.' and isfile(c_localpath):
                i, created = Image.objects.get_or_create(path=c_path)
                if i.status == 1:
                    return i
            elif c_file[0] != '.':
                sub = self.get_image(c_localpath, c_path)
                if sub:
                    return sub
        return None

    def count(self, localpath):
        imgcount = 0
        dircount = 0
        contained_files = os.listdir(localpath)
        for c_file in contained_files:
            c_localpath = join(localpath, c_file)
            if c_file[0] == '.':
                continue
            if isfile(c_localpath):
                imgcount += 1
            else:
                dircount += 1
        return (imgcount, dircount)

    def list(self):
        dir = join(settings.PRIMITIVE_GALLERY['IMAGE_ROOT'], self.subfolder)
        list = os.listdir(dir)
        ret = []
        for file in list:
            if file[0] == '.':
                continue
            localpath = join(dir, file)
            path = join(self.subfolder, file)
            if isfile(localpath):
                i, created = Image.objects.get_or_create(path=path)
                ret.append({'isfile': True,
                            'name': i.name(),
                            'url': i.url(),
                            'medium': i.url('medium'),
                            'small': i.url('small'),
                            'thumbnail': i.url('thumb'),
                            'taken': i.taken(),
                            'dir': i.dir(),
                            'id': i.pk,
                            })
            else:
                name = file.replace('_', ' ')
                folder = {'isfile': False,
                          'name': name,
                          'url': path,
                          'taken': timezone.now(),
                          }
                i = self.get_image(localpath, path)
                if i:
                    folder['medium'] = i.url('medium')
                    folder['small'] = i.url('small')
                    folder['thumbnail'] = i.url('thumb')
                    folder['taken'] = i.taken()

                imgcount, dircount = self.count(localpath)
                folder['imgcount'] = imgcount
                folder['dircount'] = dircount
                ret.append(folder)
        ret.sort(key=lambda file: file['taken'])
        return ret
