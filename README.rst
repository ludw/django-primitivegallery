django-primitivegallery
=======================

A simple and primitive gallery for django.

This project is currently in alpha and not intended for production use.

Requirements
------------

The following packages must be installed:

- Django >= 1.5
- Pillow or PIL
- ImageMagick
- jhead


Installation
------------
1. Make sure the requirements above are installed. The first two can be installed with pip, the rest can be found in apt-get if you are using a debian based system.

2. Add ``primitivegallery`` to your ``INSTALLED_APPS``

3. Add the following settings:

::

  PRIMITIVE_GALLERY = {
      'IMAGE_ROOT': os.path.join(BASE_DIR, 'images'),
      'IMAGE_URL': '/static/'
  }

Where ``IMAGE_ROOT`` is the path to your images on disk and ``IMAGE_URL`` are the path the webserver serves them on.

4. Import the primitivegallery urls on some path in your urls.py file:

::

  url(r'^', include('primitivegallery.urls')),
