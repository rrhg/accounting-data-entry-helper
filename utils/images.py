from PIL import Image
import cv2
import io

def image_to_bytes(img):
    return img.tobytes()
    # >>> img = Image.open(f)
    # >>> img.show()
    # >>> bytes = img.tobytes()
    # >>> img2 = Image.frombytes(img.mode, img.size, bytes)
    # >>> img2.show() # worked

def bytes_toImage(mode, size, bytes):
    return Image.frombytes(mode, size, bytes)
    # >>> img = Image.open(f)
    # >>> img.show()
    # >>> bytes = img.tobytes()
    # >>> img2 = Image.frombytes(img.mode, img.size, bytes)
    # >>> img2.show() # worked


def image_to_string(img):
    # img = Image.open("test.png")
    buf = io.BytesIO()
    img.save(buf, format="png")
    image_as_string = base64.b64encode(buf.getvalue())
    return image_as_string

def string_to_image(image_as_string):
    img=Image.open(io.BytesIO(base64.b64decode(image_as_string)))
    return img


def convert_multi_page_pdf_to_pil_imgs_pages(pdf_strpath):
    from pdf2image import convert_from_path
    pages_pil_imgs = convert_from_path(pdf_strpath)
    return pages_pil_imgs


def convert_pil_img_to_cv2(pil):
    import numpy
    # pil_image = PIL.Image.open('Image.jpg').convert('RGB') 
    open_cv_image = numpy.array(pil) 
    # Convert RGB to BGR
    cv2 = open_cv_image[:, :, ::-1].copy()
    return cv2

class ResizeImage():

    def __init__(self, imgH=64, imgW=3072, keep_ratio_with_pad=True):
        self.imgH = imgH
        self.imgW = imgW
        assert keep_ratio_with_pad == True
        self.keep_ratio_with_pad = keep_ratio_with_pad

    def __call__(self, im):        

        old_size = im.size  # old_size[0] is in (width, height) format

        ratio = float(self.imgH)/old_size[1]
        new_size = tuple([int(x*ratio) for x in old_size])
        im = im.resize(new_size, Image.BICUBIC)

        new_im = Image.new("RGB", (self.imgW, self.imgH))
        new_im.paste(im, (0, 0))

        return new_im

