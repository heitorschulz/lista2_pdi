
from PIL import Image
import numpy as np
import math
import cv2
import matplotlib.pyplot as plt



def calculo_limiar_global(imagem,dT):
    T = np.mean(imagem)   #Limiar T atual
    T_ant = 0 #Limiar T anterior

    #count=0
    #Enquanto a diferença do limiar atual e anterior não menor que o parâmetro dT, repete. 
    while(np.abs(T-T_ant)>dT):
        #Segmentar a imagem usando o limiar T em dois grupos G1 e G2, sendo que 
        #em G1 tem pixels com intensidade > T, e
        #em G2 tem pixels com intensidade <= T.
        G1=imagem[imagem>T]
        G2=imagem[imagem<=T]
        
        # count+=1
        # print("Iteracao:",count)

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
    imgGTT.save('output/4.1-GTT_h'+'.jpg')

    imgLET = Image.fromarray(np.uint8(imageLET))
    imgLET.save('output/4.1-LET_h'+'.jpg')

    return 


def segmentacao_otsu(imagem, limiar,img_orig):
    imgGTT = Image.new(img_orig.mode, img_orig.size, color = 'black')
    imgLET = Image.new(img_orig.mode, img_orig.size, color = 'black')
    print("modo:",img_orig.mode)

    imageGTT = np.asarray(imgGTT,dtype='float64')
    imageLET = np.asarray(imgLET,dtype='float64')

    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            if(imagem[i,j]>limiar):
                imageGTT[i,j]=imagem[i,j]
            else:
                imageLET[i,j]=imagem[i,j]

    imgGTT = Image.fromarray(np.uint8(imageGTT))
    imgGTT.save('output/4.2-OTSU_GTT_h'+'.jpg')

    imgLET = Image.fromarray(np.uint8(imageLET))
    imgLET.save('output/4.2-OTSU_LET_h'+'.jpg')

    return 


def calculo_limiar_otsu(imagem):

    p = np.zeros(256, dtype='float64')
    P = np.zeros(256, dtype='float64')
    m = np.zeros(256, dtype='float64')
    var = np.zeros(256, dtype='float64')

    #1 Passo: Calculo das probabilidades p
    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            p[int(imagem[i,j])]+=1
    
    p=p/(imagem.shape[0]*imagem.shape[1])

    #2 Passo: Calculo das somas acumuladas
    P[0]=p[0]
    for i in range(255):
        P[i+1]=p[i+1]+P[i]

    #3 Passo: Media
    m[0]=0
    for i in range(255):
        m[i+1]=(i+1)*p[i+1]+m[i]
    
    #4 Passo: Media geral
    mg=m[255]

    #5 Passo: Calculo da variancia
    constante=0.000001
    varMax=0
    iMax=0
    for i in range(256):
        var[i]=(((mg*P[i])-m[i])**2)/((P[i]*(1-P[i]))+constante)
        #6 Passo: Achar a máxima variancia
        if(var[i]>varMax):
            varMax=var[i]
            iMax=i

    return iMax


def filtragem_homomorfica(filepath):

    img = cv2.imread(filepath,-1)
    img = np.float32(img)
    img = img/255

    rows,cols,dim=img.shape

    rl, rh, cutoff = 0.3,1.01,1

    imgYCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

    y,cr,cb = cv2.split(imgYCrCb)
    channels = cv2.split(imgYCrCb)

    y_log = np.log(y+0.01)

    y_fft = np.fft.fft2(y_log)

    y_fft_shift = np.fft.fftshift(y_fft)


    DX = cols/cutoff
    G = np.ones((rows,cols))
    for i in range(rows):
        for j in range(cols):
            G[i][j]=((rh-rl)*(1-np.exp(-((i-rows/2)*2+(j-cols/2)*2)/(2*DX*2))))+rl

    result_filter = G * y_fft_shift

    result_interm = np.real(np.fft.ifft2(np.fft.ifftshift(result_filter)))

    result = np.exp(result_interm)
    result = result.astype(y.dtype)

    cv2.merge([result,cr,cb],imgYCrCb)

    imgRGB = cv2.cvtColor(imgYCrCb, cv2.COLOR_YCrCb2BGR)

    imgRGB2=np.clip(imgRGB*255,0,255)

    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist(imgRGB2,[i],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    plt.savefig('output/4h_hist.png', dpi=100)


    # for i,col in enumerate(color):
    #     histr = cv2.calcHist(img,[i],None,[256],[0,256])
    #     histr = np.clip(histr,0,130)
    #     plt.plot(histr,color = col)
    #     plt.xlim([0,256])
    # plt.savefig('output/4h_hist_o.png', dpi=100)

    #plt.imshow(imgRGB)
    #plt.show()


    cv2.imwrite('output/4h_img.jpg',imgRGB2)





def main():


    filtragem_homomorfica('input/rice.jpg')
    
    #fileImage = Image.open('input/rice.jpg')
    fileImage = Image.open('output/4h_img.jpg')
    image = np.asarray(fileImage, dtype='float64')

    dT=2
    T=calculo_limiar_global(image,dT)

    if(fileImage.mode=='RGB'):
        segmentacao_limiar_global(image[:,:,0], T,fileImage)
        T_Otsu=calculo_limiar_otsu(image[:,:,0])
        segmentacao_otsu(image[:,:,0],T_Otsu,fileImage)
    else:
        segmentacao_limiar_global(image, T,fileImage)
        T_Otsu=calculo_limiar_otsu(image)
        segmentacao_otsu(image,T_Otsu,fileImage)

    
    print("Global Simples:",T, "com dT=",dT ,"|| OTSU:",T_Otsu)
    return



if __name__ == '__main__':
    main()