import os
from Image_Reader import ImageReader
from DCT_Classic import DCT
import Quantum_Subroutines
import os
import Image_Compression
import cv2
import matplotlib.pyplot as plt
import numpy as np

# print(
#     os.listdir(
#         "C:/Users/John/Documents/GitHub/qaoa_testing_framework/StateCompression/images/misc/"
#     )
# )

fileNames = os.listdir("StateCompression/images/misc/misc")

compressionLevels = list(range(0, 13))
psnr = {}
sip = {}
for i in compressionLevels:
    psnr[i] = []
    sip[i] = []

for f in fileNames:
    print(f)
    path = "StateCompression/images/misc/misc/" + f
    image = ImageReader.getImage(path)
    N = image.shape[0]
    dct = DCT.normal1D(N)
    imageNorm = np.linalg.norm(image)
    normalizedImage = image / imageNorm

    for level in compressionLevels:
        rC = 2 ** ((level + 1) // 2)
        cC = 2 ** (level // 2)

        # print(rC, cC)

        compressedImage = Image_Compression.naiveDCTCompression(image, N, rC, cC)
        norm = np.linalg.norm(compressedImage)
        normData = compressedImage / norm
        remade = DCT.remakeImage(normData, dct)
        inner = np.inner(remade.flatten(), normalizedImage.flatten()) ** 2
        # if inner >= 1:
        #     print(inner, level)
        # imageRemade = remade * norm
        # psnrVal = cv2.PSNR(image.astype(int), imageRemade.astype(int))
        # psnr[level].append(psnrVal)
        sip[level].append(inner)

    #     plt.title("SIP: " + str(inner))
    #     plt.imshow(imageRemade, cmap="gray")
    #     plt.figure()
    # plt.show()

# yPSNR = []
# yPSNRErr = []
yInner = []
yInnerErr = []
for i in compressionLevels:
    # p = psnr[i]
    inner = sip[i]

    # yPSNR.append(np.mean(p))
    # yPSNRErr.append(np.std(p))
    yInner.append(np.mean(inner))
    yInnerErr.append(np.std(inner))

# plt.errorbar(compressionLevels, yPSNR, yPSNRErr)
# plt.title("PSNR under compression rounds C")
# plt.xlabel("C")
# plt.ylabel("PSNR")
# plt.savefig("psnr")

# plt.figure()
plt.errorbar(compressionLevels, yInner, yInnerErr)
plt.title("|⟨ψ|φ⟩|^2 under compression rounds C")
plt.xlabel("C")
plt.ylabel("|⟨ψ|φ⟩|^2")
plt.savefig("sip")
plt.show()
