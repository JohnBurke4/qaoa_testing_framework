import math
import numpy as np

class DCT:

    def normal1D(N):
        a0 = 1  / np.sqrt(N)
        a1 = np.sqrt(2/N)

        result = np.zeros((N, N))

        for u in range(0, N):
            for n in range(0, N):
                coef = a1
                if u == 0:
                    coef = a0

                result[u, n] = coef * np.cos((2*n + 1) * u * np.pi / (2 * N))

        return result

    def getDCTBitcount(dct):
        max = np.amax(dct)
        return int(math.log2(max)) + 1

    def int1D(N, precision):
        a0 = 1 / math.sqrt(N)
        a1 = math.sqrt(2/N)

        result = np.zeros((N, N), dtype=int)

        for u in range(0, N):
            for n in range(0, N):
                coef = a1
                if u == 0:
                    coef = a0

                result[u, n] = int(
                    (2**precision) * coef * np.cos((2*n + 1) * u * np.pi / (2 * N)))

        return result

    def convertImage(image, dct, precision=None):
        if (precision):
            return (np.matmul(np.matmul(dct, image).astype(int) / 2**(precision), np.transpose(dct)).astype(int) / 2**(precision))
        return np.matmul(np.matmul(dct, image), np.transpose(dct))

    def convertImage1D(image, dct, precision=None):
        return np.matmul(dct, image)

    def convertImage2D(image, dct):
        return np.matmul(np.matmul(dct, image), np.transpose(dct))

    def remakeImage(image, dct, precision=None):
        if (precision):
            return (np.matmul(np.matmul(np.transpose(dct).astype(int) / 2**(precision), image), dct).astype(int) / 2**(precision))
        return np.matmul(np.matmul(np.transpose(dct), image), dct)

    def removeSmallBits(chunk):
        chunk[abs(chunk) < 100] = 0
        return chunk


