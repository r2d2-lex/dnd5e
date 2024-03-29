import io
import sys

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
import datetime
import requests


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'


def get_html(url):
    headers = {'User-Agent': USER_AGENT}
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Network err...")
        return False


def str2bool(v):
    if isinstance(v, bool):
        return v
    return v.lower() in ("yes", "true", "t", "1", "on")


def get_date_time(template):
    return datetime.datetime.now(tz=timezone.utc).strftime(template)


def resize_image(image, fixed_width, image_field_name):
    img_opened = Image.open(image)
    width_percent = (fixed_width / float(img_opened.size[0]))
    height_size = int((float(img_opened.size[0]) * float(width_percent)))
    img_opened = img_opened.convert('RGB')
    new_image = img_opened.resize((fixed_width, height_size))
    # image = models.FileField() only takes Fileupload object
    output = io.BytesIO()
    new_image.save(output, format='JPEG', quality=85)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField',
                                image_field_name,
                                'image/jpeg',
                                sys.getsizeof(output), None)
