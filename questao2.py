from PIL import Image
import numpy as np


def equalizacao_histograma(array):
    valor_minimo = np.amin(array)
    array = array - valor_minimo

    valor_maximo = np.amax(array)
    array = array * 255/valor_maximo

    return array


def main():

    fileImage = Image.open('input/baixo_contraste.jpg')
    image = np.asarray(fileImage,dtype='float64')

    R_array=image[:,:,0]
    G_array=image[:,:,1]
    B_array=image[:,:,2]
    
    R_array=equalizacao_histograma(R_array)
    G_array=equalizacao_histograma(G_array)
    B_array=equalizacao_histograma(B_array)
    
    image[:,:,0]=R_array
    image[:,:,1]=G_array
    image[:,:,2]=B_array

    img = Image.fromarray(np.uint8(image))
    img.save('output/baixo_contraste.jpg')

    return 0





if __name__ == '__main__':

    main()
