"""
Lista 2 de Processamento Digital de Imagens
Questão 05
Aluno: Heitor Schulz
Matricula: 2016101758
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import cmath
from math import sqrt, exp

def shift(a_fft):
    b_fft = np.zeros((a_fft.shape[0],a_fft.shape[1]),dtype=complex)
    for i in range(a_fft.shape[0]):
        for j in range(a_fft.shape[1]):
            b_fft[i,j] = a_fft[i,j] * (-1)**(i+j)
    return b_fft

#Algoritmo de linha de Bresenham's
# Produz uma lista de tuplas com os pontos de uma linha do ponto "start" até o ponto "end"
def get_line(start, end):
   
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


#calcula Sr para diversos raios
def calcula_Sr(img_fft):

    valores=[]
    cx = int(img_fft.shape[0]/2)
    cy = int(img_fft.shape[1]/2)
    r_max=int(np.amin([img_fft.shape[0],img_fft.shape[1]])/2)

    valores.append(img_fft[cx,cy])

    for raio in range(r_max-1):
        
        raio+=1
        angRad = np.pi/2
        x_ant=0
        y_ant=0

        somatorio=0

        while angRad < 1.5*np.pi:
            x = int(cx + raio*np.cos(angRad))
            y = int(cy + raio*np.sin(angRad))

            if(x_ant!=x or y_ant!=y):
                somatorio+=img_fft[x,y]
                x_ant=x
                y_ant=y

            angRad+=1/(2*raio)
        valores.append(somatorio)

    return valores

#Calcula S(theta) para o raio maximo
def calcula_So(img_fft):
    valores=[]
    cx = int(img_fft.shape[0]/2)
    cy = int(img_fft.shape[1]/2)
    r_max=int(np.amin([img_fft.shape[0],img_fft.shape[1]])/2)

    raio=r_max-1
    angRad = np.pi/2
    x_ant=0
    y_ant=0

    somatorio=0

    while angRad < 1.5*np.pi:
        x = int(cx + raio*np.cos(angRad))
        y = int(cy + raio*np.sin(angRad))
        if(x_ant!=x or y_ant!=y):
            pontos=get_line((cx,cy),(x,y))
            somatorio=0
            for coordenada in pontos:
                somatorio+=img_fft[coordenada[0],coordenada[1]]
            valores.append(somatorio)
            x_ant=x
            y_ant=y

        angRad+=1/(2*raio)
    return valores


def exercicio5(imagem1, nome):

    img_shift_1 = shift(imagem1)
    img_fft_1 = np.fft.fft2(img_shift_1)

    plt.figure(figsize=(20, 12), constrained_layout=False)
    plt.subplot(221), plt.imshow(imagem1, "gray"), plt.title("Imagem 1 Original")
    plt.subplot(222), plt.imshow(np.log(np.abs(img_fft_1)), "gray"), plt.title("Espectro 1")

    val=calcula_Sr(np.abs(img_fft_1))
    plt.subplot(223), plt.plot(val),plt.title("S(r)")
    val2=calcula_So(np.abs(img_fft_1))

    custom_x=np.linspace(0,180,len(val2))
    plt.subplot(224), plt.plot(custom_x,val2),plt.title("S(o)")
    plt.savefig("output/"+nome+"_info.png",dpi=300)
    #plt.show()
    


def main():

    img1=cv2.imread("input/Fig8.02(a).jpg", 0)
    img2=cv2.imread("input/Fig8.02(b).jpg", 0)

    exercicio5(img1,"5_a")
    exercicio5(img2,"5_b")

    return


if __name__ == '__main__':
    main()
