import numpy as np
from DCT_Classic import DCT

def naiveDCTCompression(image, N, rC, cC):
    dct = DCT.normal1D(N)

    compressedImage = DCT.convertImage2D(image, dct)

    r = int(N / rC)
    c = int(N / cC)

    if (r > c):
        compressedImage[r:,:] = 0
        compressedImage[:,c:] = 0
    else:
        compressedImage[:,c:] = 0
        compressedImage[r:,:] = 0
    
    # print(compressedImage[compressedImage != 0])

    return compressedImage



