import os 

import numpy as np 
import cv2 as cv

VALID_FORMAT = [".jpg", ".jpeg", ".jp2", ".png", ".bmp", ".tiff", ".tif"]


def canny(image, sigma=0.33):
    # Compute the median of the single channel pixel intensities
    median = np.median(image)

    lower = 0
    upper = 0

    if median > 191:
        lower = int(max(0, (1.0 - 2 * sigma) * (255 - median)))
        upper = int(max(85, (1.0 + 2 * sigma) * (255 - median)))
    elif median > 127:
        lower = int(max(0, (1.0 - sigma) * (255 - median)))
        upper = int(min(255, (1.0 + sigma) * (255 - median)))
    elif median < 63:
        lower = int(max(0, (1.0 - 2 * sigma) * median))
        upper = int(max(85, (1.0 + 2 * sigma) * median))
    else:
        lower = int(max(0, (1.0 - sigma) * median))
        upper = int(min(255, (1.0 + sigma) * median))

    edge = cv.Canny(image, lower, upper)
    return edge


def otsu(image):
	upper, otsu = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
	lower = 0.5 * upper

	edge = cv.Canny(image, lower, upper)
	return edge


def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    blurred = cv.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)

    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
		
    return sharpened


def valid_path(path):
	return os.path.isfile(path)


def get_extention(path):
	return os.path.splitext(path)[1].lower()


def valid_imgage(path):
	if not valid_path(path):
		return False 
	else:
		extention = get_extention(path)

		if extention not in VALID_FORMAT:
			return False 
		
		return True
