import time
from PyPDF2 import PdfFileReader, PdfFileWriter
from utils.pdf.scale_pdf import scale_pdf
# from pdf2image import convert_from_path
from config import ( STATEMENT_DATA_FILE, STATEMENT_PDF,
                     PATH_TESSERACT_IMAGES_DIR,
                     IMPROVED_STATEMENT_PDF, client_name, client)
from rich.console import Console

red = Console(style="red")
yellow = Console(style="yellow")



def improve_pdf(input_path, output_path):
    """
        Try to improve PDF to be converted to text by Tesserac
        - https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html

        Important: PDFs are not original. 
            - are scanned or copied.
    """

    if ( hasattr(client, 'rm_pdf_page')
         or
         hasattr( client, 'rm_last_pdf_pages')
    ):
        from utils.pdf.rm_pdf_page import rm_pdf_page
        rm_pdf_page(
            page_to_remove = client.rm_pdf_page(),
            rm_last_pdf_pages = client.rm_last_pdf_pages(),
            in_file_path = str(STATEMENT_PDF), # in
            out_file_path = str(IMPROVED_STATEMENT_PDF) # out
        )
        input_path = str(IMPROVED_STATEMENT_PDF) # change to use pdf w removed page

    if hasattr(client, 'scale_bank_pdf_to'):
        scale_factor, increase_page_width, move_right = (
            client.scale_bank_pdf_to()
        )
    else: 
        scale_factor = 1.04
        increase_page_width = 20
        move_right=5 # crop the pdf. move left top corner to the right. as in do not include the first pixels at the left . like scaning the pdf but do not start at left marging, start a little bit to the right, so that white space in the left is not included

    red.print(f'\nScaling to {scale_factor} % ==> ');print( input_path );print()
    red.print(f'\nAnd copying to ==> ');print( output_path );print()

    scale_pdf( 
            input_path=input_path,
            output_path=output_path,
            scale_factor=scale_factor,
            move_right=move_right,
            increase_page_width=increase_page_width
    )

    # do not delete
    # rotating:
    #        or maybe with opencv https://pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/
    #        the problem is in python only found to do it by 90 degrees with PyPDF2. didnt found other way to do it. aparently with latex u can
    #        maybe subprocess.run('some latex program that can rotate by 1 degree')

    # do not delete
    # background:
    #        could be improve in 2 ways. Read code in:
    #            - from utils.clean_img import clean_img
    #        need to convert each pdf page to an img & clean it with opencv or ImageMagic
    #        It's been done in pdf2txt.py right before tesseract reads the image

    time.sleep(1)