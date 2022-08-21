import base64, io
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
import cv2
import pytesseract
from pdf2image import convert_from_path

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo

# Hugginface TrOCR
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

from config import PERIOD, client, STATEMENT_PDF, CHECKS_IMAGES_DIR, client_name
from utils.suppress_io import suppress_stdout, suppress_stderr
from utils.images import convert_pil_img_to_cv2, ResizeImage
from utils.images import image_to_string, string_to_image
from utils.other import ask_to_continue
from db.models import CkImage

from rich.console import Console
red = Console(style="red")
yellow = Console(style="yellow")


yellow.print("\n Instantiating gigantic cks_images module !! \n")
yellow.print("\n Extracting cks imgs from statement pdf, payee imgs from ==> cks imgs, & ck number from cks imgs \n")



# Detectron2 pretrained models
d2_checks_model = client.d2_checks_model
d2_ck_number_model = client.d2_ck_number_model


# Hugginface TrOCR
# not going to fine tune for now bc 1- will start saving payee images under vendor so later I have enough images. 2- Right now need to start gettting some data entry done.
# think it downloads pre trained model only once bc when I change it from base to large, it started downloading a lot of stuff(pytorch_model.bin, configs, etc) & I don't remember seen that never, maybe except for the 1st time I used the base
"""how to improve in the future. maybe only by fine tunning. I will have the payee images by vendor. I tried resizing images but apparently won't do much"""

# with suppress_stderr(): # print lots of warnings
with suppress_stdout(): # print lots of warnings
    # hugginface_TrOCR_processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten") 
    hugginface_TrOCR_processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-handwritten") 
    # hugginface_TrOCR_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
    hugginface_TrOCR_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-large-handwritten")



def extract_and_save(client, use_textract=False):

    # if this_period_was_done(): # DONE in convert_checks_lines... so we don't have to instantiatiate this module if was done

    cks_pil_imgs = get_cks_pil_imgs_from_statement()
    get_db_instances_list(d2_ck_number_model, cks_pil_imgs, use_textract=use_textract)


def get_cks_pil_imgs_from_statement():
    red.print(f"\n Extracting checks images from: {str(STATEMENT_PDF)}\n")
    statement_pages_pil_imgs = convert_from_path(str(STATEMENT_PDF))
    cks_imgs = []
    for pg in statement_pages_pil_imgs:
        extracted = extract_images(pg, d2_checks_model)
        cks_imgs.extend(extracted)
        # save_imgs_to_dir(cks_imgs, CHECKS_IMAGES_DIR) # when we get it
    return cks_imgs


def get_db_instances_list(d2_ck_number_model: Path, cks_pil_imgs, use_textract=False):
    red.print(f"\n Creating list of checks with images & data\n")
    cks_imgs = []
    for i, img in enumerate(cks_pil_imgs):
        # ck = Check(i,img, d2_ck_number_model, use_textract=use_textract)
        ck_img = create_ck_img_db_model_instance(i, img)
        ck_img.save_to_db(client_name) # each one has an sqlalchemy relationship with a client
        cks_imgs.append(ck_img)
    return cks_imgs


def create_ck_img_db_model_instance(index, ck_image, use_textract=False):

    alt_number = str(index) 
 
    ck_number_img = extract_ck_numb_img(ck_image) 
    # payee_img_path = better done in CKImage class method so that can be called with the vendor name, # payee_img_path = save_payee_img_in_dir(payee_img) # done in class
    ck_number = str(infer_number_from_ck_numb_img(ck_number_img)) 
    path = save_ck_img_in_dir(ck_image, ck_number, alt_number) 

    payee_img = crop_payee(ck_image, client_name) 
    payee_img_as_bytes = payee_img.tobytes() # bc when we have the vendor, is when will save it to a folder for just that vendor, for future traini of the ml model
    payee_img_mode = payee_img.mode
    payee_img_width = payee_img.size[0]
    payee_img_height = payee_img.size[1]

    payee_txt_hugginface = infer_payee_txt_w_hugginface(payee_img) 
    if use_textract:  # this cost $$
        payee_txt_textract = infer_payee_txt_w_aws_textract(payee_img) 
    else:
        payee_txt_textract = ""

    ck = CkImage(
        period = PERIOD,
        path=path,
        ck_number = ck_number,
        alt_number = alt_number,
        payee_img_as_bytes = payee_img_as_bytes,
        payee_img_mode = payee_img_mode,
        payee_img_width = payee_img_width,
        payee_img_height = payee_img_height,
        payee_txt_hugginface = payee_txt_hugginface,
        payee_txt_textract = payee_txt_textract,
    )
    return ck


def infer_payee_txt_w_aws_textract(payee_img):
    """send img(w just 1 line of txt) bytes to aws textract"""
    import boto3 # bc we will not al
    # resized_img = self.payee_img.resize((600,100)) # with self.payee_img had twice better results than resized_img. Not sure why. Some resized did not got results at all. 
    # resized_img.save(buf, format='JPEG')

    buf = io.BytesIO()
    payee_img.save(buf, format='JPEG')
    byte_im = buf.getvalue()
    textract = boto3.client('textract')
    response = textract.analyze_document(
        Document={'Bytes': byte_im,},
        FeatureTypes=['FORMS',],
    )
    try:
        txt = response['Blocks'][1].get('Text') # bc img has only 1 line
    except:
        txt = 'textract not found'
    return txt


def infer_payee_txt_w_hugginface(payee_img):
    """how to improve in the future. maybe only by fine tunning. I will have the payee images by vendor. I tried resizing images but apparently won't do much"""
    # print(self.payee_img.size) # 370, 43
    
    resized_img = payee_img.resize((600,100)) # improved a little bit. some words are better
    # resized_img = payee_img.resize((900,150)) # not sure got any improvement over 600,100

    with suppress_stderr(): # do not print lots of warnings
        # pixels = hugginface_TrOCR_processor(self.payee_img, return_tensors="pt").pixel_values 
        pixels = hugginface_TrOCR_processor(resized_img, return_tensors="pt").pixel_values 
        ids = hugginface_TrOCR_model.generate(pixels)
        txt = hugginface_TrOCR_processor.batch_decode(ids, skip_special_tokens=True)[0] 
        return txt


# now is a method of CkImage class so can be called after we have the vendor & store it under this vendor for future model training
# def save_payee_img_in_dir(client_name: str, ck_number: str):
#     """saving under vendor for future model training"""
#     this_payee_dir = PAYEES_IMGS_DIR / vendor
#     this_payee_dir.mkdir(parents=True, exist_ok=True)
#     name =  + "_payee.jpg"
#     path = this_payee_dir / name
#     self.payee_img.save(path)


# now using models CkImage
# class Check:
#     def __init__(self, alternate_numb, pil_img, d2_ck_number_model: Path, use_textract=False ):
#         # self.ck_path = path
#         self.alternate_numb = alternate_numb
#         self.pil_img = pil_img
#         self.d2_ck_number_model = d2_ck_number_model
#         # self.cks_info_tesseract = cks_info_tesseract
#         self.number_img = self.get_number_pil_img()
#         self.number = self.infer_number_from_ck_numb_img()
#         self.save_ck_img()
#         self.payee_img = self.crop_payee()
#         self.payee_txt_hugginface = self.infer_payee_txt_w_hugginface()
#         self.payee_txt_textract = 'use_textract=False'
#         if use_textract:
#             self.payee_txt_textract = self.infer_payee_txt_w_aws_textract()

#     def show_payee_img(self):
#         self.payee_img.show()

#     def show_ck_number_img(self):
#         self.number_img.show()

#     def show_ck_img(self):
#         self.pil_img.show()



def save_imgs_to_dir(pil_imgs, directory):
    images = []
    for i, img in enumerate(pil_imgs):
        img_obj = {}
        name = f"check_{str(i)}.jpg"
        file_path = directory / name
        img.save(file_path)
        img_obj['path'] = file_path
        img_obj['pil_img'] = img
        images.append(img_obj)
    return images


def get_coordinates(img: Image, model: Path):

    def find_detectron2_images(img: Image, model: Path):
        # explicacion retrainin(fitting) Detectron to detect checks esta en grabaciones iphone
        cfg = get_cfg()
        cfg.MODEL.DEVICE = 'cpu'
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
        cfg.MODEL.WEIGHTS = str(model)  # path to the model we just trained
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set a custom testing threshold
        predictor = DefaultPredictor(cfg)

        # im = cv2.imread(str(img))
        im = convert_pil_img_to_cv2(img)
        outputs = predictor(im)
        return outputs

    def get_coordinates_of_detectron2_images(detectron2_images):
        # How to obtain the Bounding Box Co-ordinates of any predicted Object in the Image #1519
        # https://github.com/facebookresearch/detectron2/issues/1519
        boxes = detectron2_images["instances"].pred_boxes
        all_coordinates = []
        for box in boxes.__iter__():
            coordinates = box.cpu().numpy()
            # print(coordinates)
            all_coordinates.append(coordinates)
        return all_coordinates

    found = find_detectron2_images(img, model)
    return get_coordinates_of_detectron2_images(found)


def remove_bottom_text_in_ck_number_img(pil_img):
    w, h = pil_img.size
    # print(w, h) # 702, 304 # only on 1 case
    lower = round(h * .82) # remove 18% at bottom
    # print(lower)
    # area (left, upper, right, lower)
    area = (   0,    2,    w,  lower)
    cropped_img = pil_img.crop(area)
    return cropped_img


def extract_images(img: Image, model: Path, is_ck_number=False):
    """Returns a list of PIL image objects"""
    # Extract all bounding boxes using OpenCV Python
    # https://stackoverflow.com/questions/21104664/extract-all-bounding-boxes-using-opencv-python#21108680
    coordinates = get_coordinates(img, model)
    cropped_pil_imgs = []
    for area in coordinates:
        # print(area)
        # print(type(area))
        # new_img = Image.open(str(img)) # https://stackoverflow.com/questions/9983263/how-to-crop-an-image-using-pil
        cropped_img = img.crop(area)
        if is_ck_number:
            cropped_img = remove_bottom_text_in_ck_number_img(cropped_img)
        # cropped_img.show() # opens default os app for images
        cropped_pil_imgs.append(cropped_img)
    return cropped_pil_imgs


def delete_all():

    # del hugginface_TrOCR_processor 
    # del hugginface_TrOCR_model

    for name in dir():
        print(f"\n name in dir(): {name}\n")
        if not name.startswith('_'):
            print(f"\n deleting: {name}\n")
            del globals()[name]



def save_ck_img_in_dir(img, ck_number, alt_number):
    file_name = alt_number + '_' + ck_number + ".jpg"
    path = CHECKS_IMAGES_DIR / file_name
    path = str(path) # pil img save needs a str
    img.save(path)
    return path # a str will be saved in the db


crop_payee_areas_map = [
    {"name":"vida","l":.17,"u":.30,"r":.70, "b":.44},
]

def crop_payee(ck_img, client_name):
    client = next(c for c in crop_payee_areas_map if c["name"] == client_name)
    if not client: raise Exception("\n Did not find client name in crop_payee_areas_map")
    w, h = ck_img.size
    left = round(w * client["l"]) # 
    upper = round(h * client["u"]) # 
    right = round(w * client["r"]) # 
    bottom = round(h * client["b"]) # 
    area = (left, upper,  right,  bottom)
    return ck_img.crop(area)


def extract_ck_numb_img(ck_image):
    ck_numb_imgs = extract_images(ck_image, d2_ck_number_model, is_ck_number=True)
    try: 
        img = ck_numb_imgs[0] # should be only 1 number per check
    except:
        img = None
        # print(f"\n didnt found ck number. showing ck image ")
        # self.pil_img.show()
        # ask_to_continue()
    return img


def infer_number_from_ck_numb_img(ck_number_img):
    if ck_number_img:
        tesse_conf = (
            #   r'--load_system_dawg 0' # nothing printed to txt file
            # + r' --load_freq_dawg 0' # nothing printed to txt file
            r'--psm 6' # Assume a single uniform block of text
        )
        text = pytesseract.image_to_string(ck_number_img, config=tesse_conf)
        text = text.strip()
    else:
        text = 'Detectron2 did not found ck_number_img'
    print(f"\n Infering_ck_number from ck_number_img with tesseract")
    print(f"\n ck_number: {text} \n")
    return text


# if __name__ == '__main__':
#     main()
