from django.conf.urls import patterns

urlpatterns = patterns(
    'primitivegallery.views',
    (r'^process$', 'process_image'),
    (r'^$', 'list'),
    (r'^(?P<size>thumbnails|small|medium)/(?P<subfolder>.*)$', 'list'),
    (r'^(?P<size>thumbnails|small|medium)/$', 'list'),
)
