import cv2
import utlis


import numpy as np
import cv2
ip = input("Digite o IP: ")
# Abre a Camera
vcap = cv2.VideoCapture('https://'+ip+':1024/video')

while(True):
    # Captura o Frame
    ret, frame = vcap.read()
    if frame is not None:
        # Mostra a Janela com o Frame
        cv2.imshow('frame',frame)
        # Aperta Q para Sair
        if cv2.waitKey(22) & 0xFF == ord('q'):
            break
    else:
        print ("Frame is None")
        break

vcap.release()
cv2.destroyAllWindows()
print ("Video stop")
