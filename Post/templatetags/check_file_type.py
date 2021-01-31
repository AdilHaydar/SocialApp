from django import template
import mimetypes

register = template.Library()

@register.filter(name='image_or_video')
def image_or_video(path):
    file_type = mimetypes.guess_type(path)[0]
    if 'video' in file_type:
        return False
    elif 'image' in file_type:
        return True
    else:
        return None

