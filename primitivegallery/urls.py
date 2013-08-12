from django.conf.urls import patterns, url

urlpatterns = patterns(
    'primitivegallery.views',
    (r'^process$', 'process_image'),
    (r'^$', 'list'),
    (r'^(?P<size>thumbnails|small|medium)/$', 'list'),
    (r'^(?P<size>thumbnails|small|medium)/(?P<subfolder>.*)$', 'list'),
    url(r'^slideshow/(?P<size>thumbnails|small|medium)/(?P<subfolder>.*)$', 'slideshow', name='slideshow'),
    url(r'^api/$', 'api_list', name='api_list'),
    url(r'^api/(?P<subfolder>.*)$', 'api_list', name='api_list'),
)
