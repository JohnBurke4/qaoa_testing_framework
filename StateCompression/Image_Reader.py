import numpy as np
import cv2
import os

class ImageReader:

    def getImage(path, N):
        # Read Images
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        maxSize = tuple([(int(x) - (int(x) % N)) for x in gray.shape])
        maxSize = tuple(reversed(maxSize))
        return cv2.resize(gray, maxSize)

    def displayImage(image, name):
        cv2.imshow(name, image)

    def chopUpImage(image, N):
        result = []
        size = image.shape

        for i in range(0, size[0], N):
            for j in range(0, size[1], N):
                result.append((image[i:i+N, j:j+N]).astype(int) - 128)

        return {
            "pieces": result,
            "size": size
        }

    def reconstructImage(pieces, N):
        length = pieces['size'][0]
        width = pieces['size'][1]
        vfunc = np.vectorize(setLimit)
        result = np.ndarray(shape=(length, width), dtype=np.uint8)
        index = 0
        for i in range(0, length, N):
            for j in range(0, width, N):
                # print((pieces['pieces'][index] + 128))
                result[i:i+N, j:j+N] = vfunc(pieces['pieces'][index] + 128)
                # print(result[i:i+N, j:j+N], i, j)
                index += 1
        
        return result
    TestImage = os.path.abspath("StateCompression/images/cameraman.png")
    ImageSetPaths = [
        "Image Test Sets\\artificial.pgm",
        "Image Test Sets\\big_building.pgm",
        "Image Test Sets\\big_tree.pgm",
        "Image Test Sets\\bridge.pgm",
        "Image Test Sets\cathedral.pgm",
        "Image Test Sets\deer.pgm",
        "Image Test Sets\\fireworks.pgm",
        "Image Test Sets\\flower_foveon.pgm",
        "Image Test Sets\hdr.pgm",
        "Image Test Sets\leaves_iso_200.pgm",
        "Image Test Sets\leaves_iso_1600.pgm",
        "Image Test Sets\\nightshot_iso_100.pgm",
        "Image Test Sets\\nightshot_iso_1600.pgm",
        "Image Test Sets\spider_web.pgm",
        "Image Test Sets\zone_plate.pgm",
    ]
        
def setLimit(a):
    a = a if a < 255 else 255
    return a if a > -255 else -255

