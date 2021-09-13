
import cv2
import numpy as np
import matplotlib.pyplot as plt
import cmath
from math import sqrt, exp

def centralizar(a_fft):
    b_fft = np.zeros((a_fft.shape[0],a_fft.shape[1]),dtype=complex)
    for i in range(a_fft.shape[0]):
        for j in range(a_fft.shape[1]):
            b_fft[i,j] = a_fft[i,j] * (-1)**(i+j)
    return b_fft

def descentralizar(a_fft):
    return centralizar(a_fft)

def exercicio5(imagem1, imagem2, nome):

    plt.figure(figsize=(20, 12), constrained_layout=False)

    img_centralizada_1 = centralizar(imagem1)
    img_centralizada_2 = centralizar(imagem2)

    img_fft_1 = np.fft.fft2(img_centralizada_1)
    img_fft_2 = np.fft.fft2(img_centralizada_2)

    plt.subplot(231), plt.imshow(imagem1, "gray"), plt.title("Imagem 1 Original")
    plt.subplot(232), plt.imshow(np.log(np.abs(img_fft_1)), "gray"), plt.title("Espectro 1")
    plt.subplot(233), plt.imshow(np.angle(img_fft_1), "gray"), plt.title("Angulo de Fase 1")

   
    plt.subplot(234), plt.imshow(imagem1, "gray"), plt.title("Imagem 2 Original")
    plt.subplot(235), plt.imshow(np.log(np.abs(img_fft_2)), "gray"), plt.title("Espectro 2")
    plt.subplot(236), plt.imshow(np.angle(img_fft_2), "gray"), plt.title("Angulo de Fase 2")
   
    plt.savefig("output/"+nome+"_info.png",dpi=300)
    plt.show()
    


def main():

    img1=cv2.imread("input/Fig8.02(a).jpg", 0)
    img2=cv2.imread("input/Fig8.02(b).jpg", 0)

    exercicio5(img1,img2,"5")

    return


if __name__ == '__main__':
    main()
