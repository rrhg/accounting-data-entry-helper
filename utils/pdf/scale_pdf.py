from PyPDF2 import PdfFileReader, PdfFileWriter
from utils.suppress_io import suppress_stdout, suppress_stderr
from pathlib import Path


def scale_pdf(input_path='',
              output_path='', 
              scale_factor=0, 
              move_right=0,
              increase_page_width=0):

    if not input_path or not output_path:
        raise Exception('Need to specify path for input & output files')
    if not scale_factor:
        raise Exception('Need to specify a scale factor')


    dir_to_clean = Path(output_path).parent
    for child in dir_to_clean.iterdir():
        if str(child) == str(output_path):
            pass # do not rm bc sometimes is used as input. it will be overwritten(i think?)
        elif child.is_file():
            child.unlink(missing_ok=True) # remove it

    reader = PdfFileReader(input_path)
    writer = PdfFileWriter()  # create a writer to save the updated results

    with suppress_stderr():
        # for some reason, everything here is printing a lot of pdfreader warnings

        for page in reader.pages:

            # Do not delete: could be needed
            # page.rotateCounterClockwise(5) # only accepts increments of 90

            if increase_page_width:
                # http://omz-software.com/pythonista/docs/ios/PyPDF2.html
                # page.cropBox.upperLeft = ( #  
                #     page.cropBox.getUpperLeft_x() + move_right,
                #     page.cropBox.getUpperLeft_y() + move_right,
                # )
                page.cropBox.upperRight = ( # make printable surface bigger
                    page.cropBox.getUpperRight_x() + increase_page_width,
                    page.cropBox.getUpperRight_y() + increase_page_width,
                )

            if move_right:
                page.mediaBox.upperLeft = ( # crop by moving corner to the right
                    page.mediaBox.getUpperLeft_x() + move_right,
                    page.mediaBox.getUpperLeft_y() + move_right,
                )
                page.mediaBox.upperRight = (
                    page.mediaBox.getUpperRight_x() + move_right,
                    page.mediaBox.getUpperRight_y() + move_right,
                )

                # page.trimBox.upperLeft = ( # crop by moving corner to the right
                #     page.trimBox.getUpperLeft_x() + move_right,
                #     page.trimBox.getUpperLeft_y() + move_right,
                # )
                # page.trimBox.upperRight = (
                #     page.trimBox.getUpperRight_x() + move_right,
                #     page.trimBox.getUpperRight_y() + move_right,
                # )

            page.scaleBy(scale_factor)  # float representing scale factor - this happens in-place
            writer.addPage(page)

        # this also prints lots of pdfreader warnings. that's why it's under supress out
        with open(output_path, "wb+") as f:
            writer.write(f)