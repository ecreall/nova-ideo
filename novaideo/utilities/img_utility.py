
import io
import os
from PIL import Image, ImageFilter

from novaideo import log

IMAGES_FORMATS = [{'id': 'xlarge', 'size': (400, 200)},
                  {'id': 'large', 'size': (300, 200)},
                  {'id': 'medium', 'size': (125, 188)},
                  {'id': 'small', 'size': (128, 85)},
                  {'id': 'profil', 'size': (140, 140)}]

AVAILABLE_FORMATS = [img_format['id'] for img_format in IMAGES_FORMATS] + ['blur']


def _get_multiple(height, width, h, l):
    multiple_h = float(height/h)
    multiple_l = float(width/l)
    if multiple_l <= multiple_h:
        return multiple_l

    return multiple_h


def _get_coordinates(height, width, area_height, area_width, x, y, h, l):
    multiple = _get_multiple(height, width, h, l)
    height_p = multiple * h
    width_p = multiple * l
    #width
    x_p = float(x + area_width/2 + width_p/2)
    width_diff = width - x_p
    if width_diff < 0:
        x_p = x_p + width_diff

    x_p = x_p - width_p
    if x_p < 0:
        x_p = 0

    #height
    y_p = float(y + area_height/2 + height_p/2)
    height_diff = height - y_p
    if height_diff < 0:
        y_p = y_p + height_diff

    y_p = y_p-height_p
    if y_p < 0:
        y_p = 0

    left = x_p
    upper = y_p
    right = left + width_p
    lower = upper + height_p
    return round(left), round(upper), round(right), round(lower)


def blur_img(fp, filename):
    try:
        img = Image.open(fp)
        if img.mode == 'P':
            img = img.convert('RGB')
    except OSError as e:
        log.warning(e)
        return {}

    img = img.filter(ImageFilter.GaussianBlur(radius=25))
    buf = io.BytesIO()
    ext = os.path.splitext(filename)[1].lower()
    img.save(buf, Image.EXTENSION.get(ext, 'jpeg'))
    buf.seek(0)
    return {'fp': buf,
            'id': 'blur'}


def generate_images(fp, filename,
                    dimension):
    x = dimension.get('x', 0)
    y = dimension.get('y', 0)
    deg = dimension.get('r', 0)
    area_height = dimension.get('area_height', 0)
    area_width = dimension.get('area_width', 0)
    result = []
    for img_format in IMAGES_FORMATS:
        try:
            img = Image.open(fp)
            if img.mode == 'P':
                img = img.convert('RGB')
        except OSError as e:
            log.warning(e)
            return result

        height = img.size[1]
        width = img.size[0]
        size = img_format['size']
        left, upper, right, lower = _get_coordinates(
                                        height, width, area_height,
                                        area_width, x, y, size[1], size[0])
        img = img.rotate(deg).crop((left, upper, right, lower))
        img.thumbnail(size, Image.ANTIALIAS)
        buf = io.BytesIO()
        ext = os.path.splitext(filename)[1].lower()
        img.save(buf, Image.EXTENSION.get(ext, 'jpeg'))
        buf.seek(0)
        img_data = img_format.copy()
        img_data['fp'] = buf
        result.append(img_data)

    result.append(blur_img(fp, filename))
    return result
