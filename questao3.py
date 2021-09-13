"""
Lista 1 de Processamento Digital de Imagens
Questão 02
Aluno: Heitor Schulz
Matricula: 2016101758
"""

from PIL import Image
import numpy as np
import math


# Corrige os valores do array para o intervalo de [0,255] por deslocamento e normalização
# Desloca o array pelo menor valor, dessa forma o valor mínimo vai para 0.
# E por fim normaliza pelo maior valor, dessa forma o valor máximo vai para 255.
def corrige_valores_por_shift_e_normalizacao(array):
    valor_minimo = np.amin(array)
   
    if valor_minimo < 0:
        array = array - valor_minimo

    valor_maximo = np.amax(array)
    if valor_maximo > 255:
        array = array * 255/valor_maximo

    return array

# Corrige os valores do array por meio de corte
# Valores negativos vão para 0
# Valores maiores que 255 vão para 255
def corrige_valores_por_corte(array):
    return np.clip(array,0,255)

# Rotaciona o filtro em 180 para fazer a convolução depois
def rotaciona_array_180_graus(array_entrada, m, n, array_saida):
    for i in range(m):
        for j in range(n):
            array_saida[i][(n-1)-j]=array_entrada[(m-1)-i][j]

#Realiza a convolução NxN
def convolucaonxn(imagem, filtro, constante, nome, tamanho_filtro, correcao,rotacao):

    pixels = np.asarray(imagem, dtype='float64')

    ##Rotaciona 180 Graus o filtro
    if(rotacao):
        filtro_out = filtro
        rotaciona_array_180_graus(filtro,tamanho_filtro,tamanho_filtro,filtro_out)
        filtro = filtro_out
    ##Realiza a convulação
    filenameConv = 'output/'
    img = Image.new(imagem.mode, imagem.size, color = 'black')
    pixels_n = np.asarray(img,dtype='float64')

    for i in range(imagem.size[0]):
        for j in range(imagem.size[1]):

            resultado=0
            initCounter = - int(tamanho_filtro/2)
            linha = initCounter
            coluna = initCounter
            
            for ii in filtro:
                for jj in ii:

                    pos_y=i+linha
                    pos_x=j+coluna
                    ##Trata Bordas aqui
                    if(pos_y<0):
                        pos_y=0
                    if(pos_x<0):
                        pos_x=0
                    if(pos_y>=imagem.size[0]):
                        pos_y=imagem.size[0]-1
                    if(pos_x>=imagem.size[1]):
                        pos_x=imagem.size[1]-1
                    resultado+=pixels[pos_x, pos_y]*jj
                    
                    coluna+=1
                
                coluna = initCounter
                linha+=1
            
            pixels_n[j,i]=resultado*constante
    
    if(correcao):
        pixels_n = corrige_valores_por_shift_e_normalizacao(pixels_n)
    else:
        pixels_n = corrige_valores_por_corte(pixels_n)    

    img = Image.fromarray(np.uint8(pixels_n))
    img.save(filenameConv+nome+'.jpg')

    return img


def main():
    #Filtro: Passa-Baixa 3x3
    Constante_Passa_Baixa_3x3 = 1/9
    Filtro_Passa_Baixa_3x3 = [[1, 1, 1],
                              [1, 1, 1],
                              [1, 1, 1]]

    #Filtro: Gaussiano 3x3
    Constante_Gaussiano_3x3 = 1/16
    Filtro_Gaussiano_3x3 = [[1, 2, 1],
                            [2, 4, 2],
                            [1, 2, 1]]

    #Filtro: Laplaciano 3x3
    Constante_Laplaciano_3x3 = 1
    Filtro_Laplaciano_3x3 = [[0,  1, 0],
                             [1, -4, 1],
                             [0,  1, 0]]           

    #Filtro: Laplaciano 45Graus 3x3
    Constante_Laplaciano_3x3_45g = 1
    Filtro_Laplaciano_3x3_45g = [[-1, -1, -1],
                                 [-1,  8, -1],
                                 [-1, -1, -1]] 

    #Filtro: Sobel 3x3 em X
    Filtro_Sobel_3x3_x = [[-1,  0, 1],
                          [-2,  0, 2],
                          [-1,  0, 1]]
    
    #Filtro: Sobel 3x3 em Y
    Filtro_Sobel_3x3_y = [[ 1,  2,  1],
                          [ 0,  0,  0],
                          [-1, -2, -1]]

    imagem = Image.open('input/Fig10.10(a).jpg')

    #usar borramento mais agressivo
    temp=convolucaonxn(imagem,Filtro_Passa_Baixa_3x3,Constante_Passa_Baixa_3x3,"tmp",3,False,True)
    convolucaonxn(temp,Filtro_Sobel_3x3_x,1,"3_Sobel_x_com_blur",3,False,False)
    convolucaonxn(imagem,Filtro_Sobel_3x3_x,1,"3_Sobel_x",3,False,False)
    convolucaonxn(imagem,Filtro_Sobel_3x3_y,1,"3_Sobel_y",3,False,False)

    return

if __name__ == '__main__':
    main()