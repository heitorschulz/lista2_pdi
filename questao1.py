# Questão 1
# Heitor Schulz
# Matricula: 2016101758

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import math
import time


def convert_rgb2hsi(imagem):
    hsi_image = np.zeros(imagem.shape, dtype='float64')
    imagem=imagem/255 #normaliza os valores de cada canal para valores entre 0 e 1
    H=S=I=0
    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            R=imagem[i,j,0]
            G=imagem[i,j,1]
            B=imagem[i,j,2]

            #Calculo do valor de H (Hue)
            numerador_h=0.5*((R-G)+(R-B))
            denominador_h=(((R-G)**2)+(R-B)*(G-B))**0.5
            constante=0.000001 #Serve para evitar divisão por zero...
            theta = math.degrees(math.acos(numerador_h/(denominador_h+constante)))
            if(B<=G):
                H=theta
            else:
                H=360.0-theta

            #Calculo do valor de S (Saturation)
            S = 1-(3/(R+G+B+constante)*np.amin([R,G,B]))

            #Calculo do valor de I (Intensity)
            I=(R+G+B)/3.0

            hsi_image[i,j]=[H,S,I]

    return hsi_image

# Corrige os valores do array por meio de corte
# Valores negativos vão para 0
# Valores maiores que 255 vão para 255
def corrige_valores_por_corte(array):
    return np.clip(array,0,255)

def convert_hsi2rgb(imagem):

    rgb_image = np.zeros(imagem.shape, dtype='float64')

    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):

            H=imagem[i,j,0]
            S=imagem[i,j,1]
            I=imagem[i,j,2]
            R=G=B=0

            aux1=I*(1-S)

            if(H>=0 and H<120):
                B=aux1
                R=I*(1+(S*math.cos(math.radians(H)))/(math.cos(math.radians(60-H))))
                G=3*I-(R+B)
            elif(H>=120 and H<240):
                H-=120
                R=aux1
                G=I*(1+(S*math.cos(math.radians(H)))/(math.cos(math.radians(60-H))))
                B=3*I-(R+G)
            else:
                H-=240
                G=aux1
                B=I*(1+(S*math.cos(math.radians(H)))/(math.cos(math.radians(60-H))))
                R=3*I-(G+B)

            rgb_image[i,j]=[R*255,G*255,B*255]

    return corrige_valores_por_corte(rgb_image)

def laranja2verde(imagem_hsi):

    for i in range(imagem_hsi.shape[0]):
        for j in range(imagem_hsi.shape[1]):
            if(imagem_hsi[i,j,0]<15):
                imagem_hsi[i,j,0]+=65
            elif(imagem_hsi[i,j,0]>=15 and imagem_hsi[i,j,0]<30):
                imagem_hsi[i,j,0]+=50
            elif(imagem_hsi[i,j,0]>=30 and imagem_hsi[i,j,0]<45):
                imagem_hsi[i,j,0]+=35
            elif(imagem_hsi[i,j,0]>=45 and imagem_hsi[i,j,0]<60):
                imagem_hsi[i,j,0]+=20
            elif(imagem_hsi[i,j,0]>=60 and imagem_hsi[i,j,0]<75):
                imagem_hsi[i,j,0]+=5

def laranja2verde_2(imagem_hsi):

    for i in range(imagem_hsi.shape[0]):
        for j in range(imagem_hsi.shape[1]):
            if(imagem_hsi[i,j,0]<65):
                imagem_hsi[i,j,0]=80


def main():
    
    fileImage = Image.open('input/oranges.jpg')
    image = np.asarray(fileImage,dtype='float64')

    imagem_em_hsi=convert_rgb2hsi(image)

    #laranja2verde(imagem_em_hsi)
    laranja2verde_2(imagem_em_hsi)

    imagem_em_rgb=convert_hsi2rgb(imagem_em_hsi)

    img = Image.fromarray(np.uint8(imagem_em_rgb))
    img.save('output/oranges.jpg')

    plt.figure(figsize=(6.4*5, 4.8*5), constrained_layout=False)
    plt.subplot(121), plt.imshow(np.uint8(image)), plt.title("Original")
    plt.subplot(122), plt.imshow(img), plt.title("Alterada")
    plt.show()
    return 0

if __name__ == '__main__':
    #init_time= time.time()
    main()
    #print("Total time:%s"%(time.time()-init_time))