import numpy as np 
import cv2 as cv
import utils

class SliceImage:
    def __init__(self, image, row, column):
        self.image = image 
        self.pieces = []
        self.row = row 
        self.column = column 


    def divide(self):
        height = self.image.shape[0]
        width = self.image.shape[1]

        height_unit = round(height / self.column)
        width_unit = round(width / self.row)

        self.pieces = []

        for i in range(0, self.row):
            pieceRow = []
            for j in range(0, self.column):
                item = self.image[i * height_unit: i * height_unit + height_unit, j * width_unit: j * width_unit + width_unit]
                pieceRow.append(item)

            self.pieces.append(pieceRow)


    def merge(self):
        rows = []
        for i in range(0, self.row):
            row = cv.hconcat(self.pieces[i])
            rows.append(row)

        self.image = cv.vconcat(rows)


    def write(self):
        for i in range(0, self.row):
            for j in range(0, self.column):
                cv.imwrite('slice/slice_' + str(i) + str(j) + ".jpg", self.pieces[i][j])


    def contrast(self):
        standard_deviations = []
        for i in range(0, self.row):
            for j in range(0, self.column):
                standard_deviation = self.pieces[i][j].std()

                if standard_deviation > 8:
                    standard_deviations.append(standard_deviation)

        return np.mean(standard_deviations)


    def edge_canny(self):
        for i in range(0, self.row):
            for j in range(0, self.column):
                self.pieces[i][j] = utils.canny(self.pieces[i][j])

    def edge_otsu(self):
        for i in range(0, self.row):
            for j in range(0, self.column):
                self.pieces[i][j] = utils.otsu(self.pieces[i][j])


    def blur(self, sigma_color, sigma_space):
        for i in range(0, self.row):
            for j in range(0, self.column):
                self.pieces[i][j] = cv.bilateralFilter(self.pieces[i][j], 9, sigma_color, sigma_space)

