import cv2


def clean_img(input_path, output_path):
    """
        Try to improve images to be converted to text by Tesserac
        - https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html

        Eliminates some background shadows in statements pdf converted to images
        Also: "improves contrast" a little bit
        Did not work well with handwritten signatures where background
        - shadows or dirt seems to have same color as real letters 
        https://medium.com/analytics-vidhya/enhance-a-document-scan-using-python-and-opencv-9934a0c2da3d

        Another way to improve contrast:
        ImageMagic; https://superuser.com/questions/622950/is-there-a-way-to-increase-the-contrast-of-a-pdf-that-was-created-by-scanning-a
    """
    image = cv2.imread(input_path, 0)

    # Otsu’s Binarization
    threshold, thresholded_image = cv2.threshold(
        image,
        0,  # threshold value, ignored when using cv2.THRESH_OTSU
        255,  # maximum value assigned to pixel values exceeding the threshold
        cv2.THRESH_BINARY + cv2.THRESH_OTSU  # thresholding type
    )

    success = cv2.imwrite(output_path, thresholded_image)
    if not success:
        raise Exception('Cleaned image was not sucessfully saved')

    # This one is creating some noise(shadows) around text
    # Do not delete. May work in another case 
    # when there is a big shadow over the entire image
    # Adaptive Thresholding 
    # thresholded_image = cv2.adaptiveThreshold(
    #     image,
    #     255,  # maximum value assigned to pixel values exceeding the threshold
    #     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # gaussian weighted sum of neighborhood
    #     cv2.THRESH_BINARY,  # thresholding type
    #     5,  # block size (5x5 window)
    #     3   # constant
    # )
