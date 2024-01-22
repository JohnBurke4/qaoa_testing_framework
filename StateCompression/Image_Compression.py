import numpy as np
from DCT_Classic import DCT

def naiveDCTCompression(image, N, rC, cC):
    dct = DCT.normal1D(N)

    compressedImage = DCT.convertImage2D(image, dct)
    # compressedImage = image.astype(int)
    

    r = int(N / rC)
    c = int(N / cC)

    # compressedImage = compressedImage + 10000

    if (r > c):
        compressedImage[r:,:] = 0
        compressedImage[:,c:] = 0
    else:
        compressedImage[:,c:] = 0
        compressedImage[r:,:] = 0

    # compressedImage = np.abs(compressedImage)
    # compressedImage[0,0] = -100

   

    
    # compressedImage = (compressedImage / 5000).astype(int)
    # print(compressedImage)
    
    # print(compressedImage[compressedImage != 0])

    return compressedImage



