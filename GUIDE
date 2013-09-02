Installing primitive gallery on a Ubuntu Server from scratch
============================================================

This guide is for setting up primitive gallery as a stand alone gallery on a Ubuntu Server with apache installed.


Installing pip
--------------

First make sure that you have a working installation of apache.

Install pip, a tool for installing python packages::

  sudo apt-get install python-setuptools

  sudo easy_intall pip


If you are fine with installing python packages globally on the server, just continue at the next heading.
If you would rather like to have your python packages isolated based on projects, take a look at virtualenv_.

.. _virtualenv: http://www.virtualenv.org


Installing requirments
----------------------
With pip install Django, Pillow and primitivegallery::

  sudo pip install django pillow django-primitivegallery

With apt-get install imagemagick and jhead::

  sudo apt-get install imagemagick jhead


Create a project
----------------
In a reasonable path where you want the gallery, issue the following command::

  django-admin startproject gallery

This will create a folder named gallery with an inner folder also named gallery. This inner folder contains a settings file and a file that routes urls. Copy these files (``settings.py`` and ``urls.py``) from the example project_ into the inner gallery folder.

.. _example project: https://github.com/ludw/django-primitivegallery/tree/master/example/example

Edit the file settings.py and make the following changes:

- Change the value of ``SECRET_KEY`` to something random and reasonably long (~50 characters).

- Turn off DEBUG mode by changing ``DEBUG`` to ``False``

- Add the hostname the gallery will be hosted on to ALLOWED_HOSTS

- Make sure the ``IMAGE_ROOT`` is correct and points to where your images are

Also take a look at the security checklist:
https://docs.djangoproject.com/en/dev/howto/deployment/checklist/


Smoke test
----------
You can make sure that everything so far is working by running the development server. In the upper gallery folder run::

  python manage.py runserver 0.0.0.0:8000

Point your browser to http://YOUR-SERVERS-IP:8000/


Configure apache
----------------
Follow the guide here to configure apache:
https://docs.djangoproject.com/en/1.1/howto/deployment/modwsgi/

Make sure that your image folder is served at the url specified in ``IMAGE_URL`` in settings.py


Add some images
---------------
Add images or folders with images to the folder you specified in the settings file.

Point your browser to the index page of the gallery.

Now change the URL to /process/ and wait until it says 'Nothing to process'.

Go back to the index page and you should have a nice gallery.
