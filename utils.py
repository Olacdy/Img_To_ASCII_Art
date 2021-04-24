import time
import numpy as np
from PIL import Image, ImageDraw
from config import ASCII, COLS, SCALE


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed


def pixels_to_chars(pixel):
    return ASCII[int((pixel * (len(ASCII))) / 255) - 1]


def get_average(arr):
    return np.average(arr.flatten())


def img_chars(img):
    new_img = []

    for i in range(img.shape[0]):
        s = ''
        for j in range(img.shape[1]):
            s += pixels_to_chars(img[i, j])
        new_img.append(s)
    return new_img


def convert_image(img_path=None, image=None):
    img = None
    if img_path is not None:
        img = Image.open(img_path).convert('L')
    if image is not None:
        img = image.convert('L')
    return np.array(img)


def chars_to_img(img_in_ascii):
    arr = np.zeros([len(img_in_ascii) * 10, len(img_in_ascii[0]) * 6, 3], dtype=np.uint8)
    arr.fill(255)
    img = Image.fromarray(arr)
    for i, row in enumerate(img_in_ascii):
        draw = ImageDraw.Draw(img)
        draw.text((0, i * 10), row, (0, 0, 0))
    return img


def get_tile_img_dim(img_size, cols=COLS, scale=SCALE):

    img_h, img_w, _ = img_size

    print("Input image dims: %d x %d" % (img_w, img_h))

    w = img_w / cols
    h = w / scale

    rows = int(img_h / h)

    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))

    if cols > img_w or rows > img_h:
        print("Image too small for specified cols!")
        exit(0)

    return w, h, cols, rows, img_w, img_h


@timeit
def get_img_in_ascii(image, tile_img_dim):

    w, h, cols, rows, img_w, img_h = tile_img_dim

    aimg = []

    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        if j == rows - 1:
            y2 = img_h

        aimg.append("")

        for i in range(cols):

            x1 = int(i * w)
            x2 = int((i + 1) * w)

            if i == cols - 1:
                x2 = img_w

            avg = int(get_average(image[y1:y2, x1:x2]))

            gsval = pixels_to_chars(avg)

            aimg[j] += gsval

    return aimg
