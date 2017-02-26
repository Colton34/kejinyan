import cv2
from ..utility.ocr import extractGrids, getRatioFromStripe, getDigitFromSequence, getAnswerFromSequence
from ..utility.io import saveToDir
from .. import settings

data_section = {
    "name": (1, 0, 1, 5),
    "id": [(4, i, 10, 1) for i in range(6)],
    "question": [(i, 1, 1, 5) for i in range(15, 25)] + [(i, 8, 1, 5) for i in range(25)]
}

def recognizeSheet(binary_image, horizontal_pos, vertical_pos):
    def getNameImage():
        '''
        return the area of image
        '''
        return extractGrids(binary_image, horizontal_pos, vertical_pos, *data_section["name"])

    def getNameImagePath():
        image = getNameImage()
        return saveToDir(image, settings.name_dir)


    def getIdImage(image_id):
        # TODO
        # extract images
        pass

    def recognizeId():
        result = list()
        for r, c, h, w in data_section['id']:
            # print (r, c, h, w)
            stripe = extractGrids(binary_image, horizontal_pos, vertical_pos, r, c, h, w)
            sequence = getRatioFromStripe(stripe, 10)
            digit = getDigitFromSequence(sequence)
            result.append(digit)
        return "".join(result).strip("-")

    # image_name = getNameImage()
    # cv2.imshow("name", image_name)
    # cv2.waitKey(0)

    def recognizeAnswer():
        result = list()
        for r, c, h, w in data_section["question"]:
            # print (r, c, h, w)
            stripe = extractGrids(binary_image, horizontal_pos, vertical_pos, r, c, h, w)
            # cv2.imshow('stripe', stripe)
            # cv2.waitKey(0)
            sequence = getRatioFromStripe(stripe, 5)
            # print (sequence)
            answer = getAnswerFromSequence(sequence)
            result.append(answer)
        return result


    result = {"id" : recognizeId(),
              "answer" : recognizeAnswer(),
              "name_image": getNameImagePath()}
    return result

