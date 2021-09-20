"""
Lista 2 de Processamento Digital de Imagens
Questão 02
Aluno: Heitor Schulz
Matricula: 2016101758
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt



def calcFreqHistograma(imagem):

    freqs = np.zeros(256)
    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            freqs[int(imagem[i,j])]+=1
    
    return freqs

def histograma(imagem,nome):
    cores=[]
    color=[]
    plt.figure(figsize=(15, 7), constrained_layout=False)


    if(imagem[0,0].size==3):
        cores=['Red Channel','Green Channel','Blue Channel',]
        color=['r','g','b']

        for i,col in enumerate(color):
            histr = calcFreqHistograma(imagem[:,:,i])
            plt.subplot(131+i), plt.plot(histr,color = col), plt.title(cores[i])
            plt.xlim([0,256])

    elif(imagem[0,0].size==1):
        histr = calcFreqHistograma(imagem)
        plt.subplot(111), plt.plot(histr,color = 'k'), plt.title('Grayscale')
        plt.xlim([0,256])

    #plt.show()
    plt.savefig('output/2_hist_'+nome+'.png', dpi=100)

    return


def equalizacao_histograma(array):
    valor_minimo = np.amin(array)
    array = array - valor_minimo

    valor_maximo = np.amax(array)
    array = array * 255/valor_maximo

    return array


def main():

    fileImage = Image.open('input/baixo_contraste.jpg')
    image = np.asarray(fileImage,dtype='float64')

    histograma(image,"antes")

    R_array=image[:,:,0]
    G_array=image[:,:,1]
    B_array=image[:,:,2]
    
    R_array=equalizacao_histograma(R_array)
    G_array=equalizacao_histograma(G_array)
    B_array=equalizacao_histograma(B_array)
    
    image[:,:,0]=R_array
    image[:,:,1]=G_array
    image[:,:,2]=B_array

    histograma(image,"depois")

    img = Image.fromarray(np.uint8(image))
    img.save('output/2_equalizacao_histograma.jpg')

    return 0

if __name__ == '__main__':

    main()
