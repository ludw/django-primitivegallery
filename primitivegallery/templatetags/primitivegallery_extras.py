from django import template

register = template.Library()

@register.filter('imageurl')
def imageurl(image, size):
    return image.url(size)
