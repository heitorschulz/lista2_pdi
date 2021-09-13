
from PIL import Image
import numpy as np
import math



def calculo_limiar_global(imagem,dT):
    T = np.mean(imagem)   #Limiar T atual
    T_ant = 0 #Limiar T anterior

    #Enquanto a diferença do limiar atual e anterior não menor que o parâmetro dT, repete. 
    while(np.abs(T-T_ant)>dT):
        #Segmentar a imagem usando o limiar T em dois grupos G1 e G2, sendo que 
        #em G1 tem pixels com intensidade > T, e
        #em G2 tem pixels com intensidade <= T.
        G1=imagem[imagem>T]
        G2=imagem[imagem<=T]

        #Calcula a intensidade média de m1 e m2 para os pixels em G1 e G2, respectivamente.
        m1=np.mean(G1) if G1.size != 0 else 0
        m2=np.mean(G2) if G2.size != 0 else 0

        #Calcula um novo limiar
        T_ant=T
        T=0.5*(m1+m2)


    return round(T)


def segmentacao_limiar_global(imagem, T,img_orig):
    imgGTT = Image.new(img_orig.mode, img_orig.size, color = 'black')
    imgLET = Image.new(img_orig.mode, img_orig.size, color = 'black')

    imageGTT = np.asarray(imgGTT,dtype='float64')
    imageLET = np.asarray(imgLET,dtype='float64')

    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            if(imagem[i,j]>T):
                imageGTT[i,j]=imagem[i,j]
            else:
                imageLET[i,j]=imagem[i,j]

    imgGTT = Image.fromarray(np.uint8(imageGTT))
    imgGTT.save('output/4.1-GTT'+'.jpg')

    imgLET = Image.fromarray(np.uint8(imageLET))
    imgLET.save('output/4.1-LET'+'.jpg')

    return 



def main():


    fileImage = Image.open('input/rice.jpg')
    image = np.asarray(fileImage,dtype='float64')

    dT=1
    T=calculo_limiar_global(image,dT)
    print("Limiar T:",T," dT:",dT)
    if(fileImage.mode=='RGB'):
        segmentacao_limiar_global(image[:,:,0], T,fileImage)
    else:
        segmentacao_limiar_global(image, T,fileImage)
    return


if __name__ == '__main__':
    main()