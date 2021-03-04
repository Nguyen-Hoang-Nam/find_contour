import numpy as np 
import cv2 as cv

from split import SliceImage
import utils

class DocumentScanner:
    def __init__(self, path):
        self.path = path 
        self.contrast = 0
        self.row = 4
        self.column = 4


    def setImage(self):
        self.image = cv.imread(self.path, 1)

    
    def copy(self):
        self.clone = self.image.copy()


    def resize(self, width):
        # old_height/old_width
        ratio = self.image.shape[0] / self.image.shape[1]

        # Only resize when image's width > 600
        if self.image.shape[1] > width:
            # Resize (width, width*ratio)
            self.image = cv.resize(self.image, (width, round(width * ratio)))


    def convertGray(self):
        self.grayscale = cv.cvtColor(self.clone, cv.COLOR_BGR2GRAY)

    
    def calculate_contrast(self):
        # Blur to decrease detail
        blur = SliceImage(self.grayscale, self.column, self.row)
        blur.divide()
        blur.blur(50, 50)
        self.contrast = blur.contrast()


    def equalization(self):
        equalization = cv.equalizeHist(self.grayscale)
        self.median = cv.medianBlur(equalization,5)

    
    def canny(self):
        self.slice.edge_canny()
        self.slice.merge()

        self.edge = self.slice.image 


    def otsu(self):
        self.slice.edge_otsu()
        self.slice.merge()
        
        self.edge = self.slice.image


    def dilate(self):
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        self.dilation = cv.dilate(self.edge, kernel, 1)

    
    def contour(self):
        contours, hierarchy = cv.findContours(self.dilation, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv.contourArea, reverse= True) 

        # Find matching contour
        for i in contours:
	        elip =  cv.arcLength(i, True)
	        approx = cv.approxPolyDP(i, 0.08*elip, True)

            # Ordinary papers have 4 corner
	        if len(approx) == 4 : 
		        doc = approx 
		        break

        cv.drawContours(self.clone, [doc], -1, (0, 255, 0), 2)


    def write(self):
        cv.imwrite('../process/grayscale.jpg', self.grayscale)
        cv.imwrite('../process/edge.jpg', self.edge)
        cv.imwrite('../process/dilation.jpg', self.dilation)
        cv.imwrite('../process/contour.jpg', self.clone)


    def test(self, name):
        cv.imwrite('result/' + name, self.clone)


    def detect(self):
        self.setImage()
        self.resize(600)
        self.copy()
        self.convertGray()

        self.slice = SliceImage(self.grayscale, self.column, self.row)
        self.slice.divide()

        self.calculate_contrast()

        if self.contrast < 25:
            self.equalization()

            self.slice.image = self.median 
            self.slice.divide()

            self.slice.blur(70, 70)
        
        else:
            self.slice.blur(50, 50)

        self.canny()
        self.dilate()
        self.contour()



    def old(self):
        
        
        #reshape to avoid errors ahead
        doc=doc.reshape((4,2))
        #create a new array and initialize 
        rect = np.zeros((4,2), dtype="float32")
        Sum = doc.sum(axis = 1)
        rect[0] = doc[np.argmin(Sum)]
        rect[2] = doc[np.argmax(Sum)]

        Diff = np.diff(doc, axis=1)
        rect[1] = doc[np.argmin(Diff)]
        rect[3] = doc[np.argmax(Diff)]

        (topLeft,topRight,bottomRight,bottomLeft) = rect

        #find distance between points and get max 
        dist1 = np.linalg.norm(bottomRight-bottomLeft)
        dist2 = np.linalg.norm(topRight-topLeft)

        maxWidth = max(int(dist1),int(dist2))

        dist3 = np.linalg.norm(topRight-bottomRight)
        dist4 = np.linalg.norm(topLeft-bottomLeft)

        maxHeight = max(int(dist3), int(dist4))

        dst = np.array([[0,0],[maxWidth-1, 0],[maxWidth-1, maxHeight-1], [0, maxHeight-1]], dtype="float32")

        M = cv.getPerspectiveTransform(rect, dst)
        warp = cv.warpPerspective(sourceImage, M, (maxWidth, maxHeight))

        destinationImage = cv.cvtColor(warp, cv.COLOR_BGR2GRAY)

        # sharpen image
        sharpen = cv.GaussianBlur(destinationImage, (0, 0), 3)
        sharpen = cv.addWeighted(destinationImage, 1.5, sharpen, -0.5, 0)
        # apply adaptive threshold to get black and white effect
        thresh = cv.adaptiveThreshold(
            sharpen, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 21, 15)
    

        cv.imwrite('scanned.jpg',  warp)
        cv.imwrite('white effect.jpg', thresh)
        return thresh
