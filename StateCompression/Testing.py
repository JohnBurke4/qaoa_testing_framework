from Image_Reader import ImageReader
from DCT_Classic import DCT
import Quantum_Subroutines
import os
import Image_Compression
import cv2
import numpy as np
from qiskit import QuantumCircuit, Aer, transpile
from qiskit_aer.backends.aerbackend import AerBackend
from qiskit.providers.fake_provider import FakeSydneyV2
from qiskit_aer import AerSimulator


N = 512
dct = DCT.normal1D(N)

image = ImageReader.getImage(ImageReader.TestImage, N)

rC = 1
cC = 1

imageNorm = np.linalg.norm(image)
normalizedImage = image / imageNorm




compressedImage = Image_Compression.naiveDCTCompression(image, N, rC, cC)
# compressedImage = np.eye(N)


norm = np.linalg.norm(compressedImage)
normData = compressedImage / norm
remade = DCT.remakeImage(normData, dct)
nQubits = int(np.log2(N*N))

aQubits =  0#int(nQubits/2)-1

totalQubits = nQubits + aQubits

qc = QuantumCircuit(totalQubits)

statePrep = Quantum_Subroutines.buildCompressedState(normalizedImage, rC, cC)

qc.append(statePrep, range(0, nQubits))
# qc.h([0, 1, 2, 3])


# qdct = Quantum_Subroutines.QDCT(int(nQubits/2), mctMode="v-chain")

# qc.append(qdct.inverse(), list(range(0, int(nQubits/2))) + list(range(nQubits, totalQubits)))
# qc.append(qdct.inverse(), list(range(int(nQubits/2), int(nQubits))) + list(range(nQubits, totalQubits)))

# qdct = Quantum_Subroutines.QDCT(int(nQubits), mctMode="recursion")

# qc.append(qdct, range(0, totalQubits))

# for i in range(0, nQubits):
#     qc.cx(nQubits+1, nQubits-i)

# qc.x(0)
# qc.h(nQubits+1)

# for i in range(0, nQubits-1):
#     qc.swap(i, i+1)


# print(qc.decompose(reps=50).depth())

sim = Aer.get_backend('aer_simulator')
# backend = FakeSydneyV2()
# aersim_backend = AerSimulator.from_backend(backend)

# circ = transpile(qc, aersim_backend)
circ = transpile(qc, sim)
circ.save_statevector()
result = sim.run(circ).result()
out_vector = result.get_statevector().data[0:N*N]

imageData = out_vector.real.reshape((N, N))
imageData = imageData

# print(dct)
# print(remade.equals(imageData))


image2 = (imageData * norm).astype(np.uint8)
image1 = (remade * norm).astype(np.uint8)

# print(image1)
# print(image2)

ImageReader.displayImage(image, "Classic Compressed")
ImageReader.displayImage(image2, "Quantum Compressed")
cv2.waitKey()




