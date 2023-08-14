import cv2  
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading
import imutils

def captura_video():
    global threshold_value, fechar, selecao

    print(threshold_value)
    # captura = video que o programa ta recebendo (0 = webcam)
    captura = cv2.VideoCapture(1)

    aruco_perimetro = 1

    run = True
    while run:
        
        #Read lê cada frame e coloca em Frame
        _, frame = captura.read()

        '''y, x = 0, 0
        h, w= 1080, 1700
        frame = frame[y:y+h, x:x+w]'''


        #detecção do aruco 
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
        parameters =  cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(dictionary, parameters)
        
        cantosAruco, id, _ = detector.detectMarkers(frame)
        cantosArucoInt = np.array(cantosAruco, dtype="int")

        if cantosAruco != ():
            cv2.polylines(frame, cantosArucoInt, True, (255, 0, 255), 5) #desenha o aruco em rosa

            #mede o tamanho do aruco em pixels 
            aruco_perimetro = cv2.arcLength(cantosAruco[0], True)

            #sabendo que o aruco tem 2cm x 2cm ele tem 8cm de perimetro
            #divide o tamanho do aruco por 8 (lado x 4), pra ter a razao de pixel/cm
            pixel_por_cm = aruco_perimetro / 8
            
        else:
            print("Mostre o aruco!")

        #print(pixel_por_cm)

        #aplica filtro de escalas de cinza
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cinza = cv2.GaussianBlur(cinza, (7, 7), 0)

        #aplica o filtro limair no frame cinza
        _, limiar = cv2.threshold(cinza, threshold_value.get(), 255, cv2.THRESH_BINARY)
        #limiar2 = cv2.adaptiveThreshold(cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


        # Detecta as bordas e executa uma dilatação + erosão 
        # para fechar as lacunas entre as bordas do objeto
        bordas = cv2.Canny(cinza, 50, 100)
        bordas = cv2.dilate(bordas, None, iterations=1)
        bordas = cv2.erode(bordas, None, iterations=1)


        #encontra contornos no Limar ou no Bordas (Canny)

        if selecao.get() == 1:
            contornos, hierarquias = cv2.findContours(limiar, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contornos, hierarquias = cv2.findContours(bordas, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        print('aa', hierarquias)
        
        #contornos = imutils.grab_contours(contornos)

        for i in range(len(contornos)):
            contorno = contornos[i]
            hierarquia = hierarquias[0][i]
            
            area = cv2.contourArea(contorno)

            if area > 1000 and area < 1200000 and hierarquia[-1] == 0:
                print(hierarquia)
                cv2.drawContours(frame, [contorno], 0, (255, 0, 0), 2)

                #cria uma caixa envolta do contono
                caixa = cv2.minAreaRect(contorno)

                #pega as cordenadas (x, y) da caixa e a largura e altura (w, h)
                (x, y), (w, h), angulo = caixa

                caixa = cv2.cv.BoxPoints(caixa) if imutils.is_cv2() else cv2.boxPoints(caixa)
                caixa = np.array(caixa, dtype="int")

                # order the points in the contour such that they appear
                # in top-left, top-right, bottom-right, and bottom-left
                # order, then draw the outline of the rotated bounding
                # desenha a caixa
                cv2.polylines(frame, [caixa.astype("int")], -2, (0, 255, 0), 2)

                #desenha um circulo azul no meio da caixa
                cv2.circle(frame, (int(x), int(y)), 10, (0,0,255), -1) 

                #converte os pixels para CM
                largura = w / pixel_por_cm
                altura = h / pixel_por_cm

                #escreve no (x, y)
                cv2.putText(frame, "Largura: {}cm".format(round(largura,1)), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
                cv2.putText(frame, "Altura: {}cm".format(round(altura,1)), (int(x), int(y+40)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
                cv2.putText(frame, "Angulo: {}".format(round(angulo,1)), (int(x), int(y+80)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)


        #imshow mostra as imagens
        cv2.imshow('Frame', cv2.resize(frame, (1100, 619)))
        cv2.imshow('Cinza', cv2.resize(cinza, (400, 225)))
        cv2.imshow('Limiar', cv2.resize(limiar, (600, 338)))
        cv2.imshow('Borda', cv2.resize(bordas, (600, 338)))


        #espera pressionar a tecla Esc para encerrar (27 = ESC)
        if cv2.waitKey(33) == 27:
            run = False
            
    cv2.destroyAllWindows()

root = tk.Tk()

threshold_value = tk.IntVar()
threshold_value.set(127)


min_val = tk.IntVar()
min_val.set(50)

max_val = tk.IntVar()
max_val.set(100)

tk.Label(root, text="Limiar:", pady=0).grid(row=1, column=1)
tk.Label(root, textvariable=threshold_value, pady=0).grid(row=1, column=2)
slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, variable=threshold_value, length=200, showvalue=0)
slider.grid(row=2, column=1,columnspan=2)

selecao = tk.IntVar()
selecao.set(1)

tk.Label(root, text="Procurar contornos em: ").grid(row=5, column=1, columnspan=2)
ttk.Radiobutton(root, text='Limiar', value=1, variable=selecao).grid(row=6, column=1)
ttk.Radiobutton(root, text='Canny', value=2, variable=selecao).grid(row=6, column=2)


fechar = True

threading.Thread(target=captura_video).start()

root.mainloop()
