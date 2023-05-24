import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened() is False:
    print("Erro ao encontrar camera")
    ip = input("Digite o Ip da camera: ")
    cap = cv2.VideoCapture('https://'+ip+':8080/video')
ret, frame = cap.read()
img_name = "1.png".format(0)
img = cv2.imwrite(img_name, frame)
# Distancia Medida da moeda até a camera
# Centimetros
t = input("Distancia do rosto até a camera: ")
t = int(t)
Known_distance = t
  
# Diametro do rosto em tamanho real
# Centimetros
i = input("diametro do rosto: ")
i = int(i)
Known_width = i
  
# Cores
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
  
# Fonte
fonts = cv2.FONT_HERSHEY_COMPLEX
  
# OBJETO para detectar a face
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
  
# função para achar o ponto focal
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):
  
    # Achando o ponto focal
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length
  
# função para estimar distancia
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
  
    distance = (real_face_width * Focal_Length)/face_width_in_frame
  
    # retornar distancia
    return distance
  
  
def face_data(image):
  
    face_width = 0  # fazer diametro do rosto zero
  
    # Converter imagem para escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
    # achar rosto na imagem
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
  
    # ciclo para achar rostos atravez da imagem
    # Achando coordenadas em x,y
    for (x, y, h, w) in faces:
  
        # Desenhar retangulo no rosto
        cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 2)
  
        # achando o diametro em pixels
        face_width = w
  
    # Retorna o diametro em pixels
    return face_width
  
  
# Le a imagem de referencia no diretorio
ref_image = cv2.imread("1.png")
  
# acha o rosto em pixels na imagem de referencia
ref_image_face_width = face_data(ref_image)
  
# acha o focal chamando a função
# diametro do rosto de referencia
# distancia previa
# tamanho previo
Focal_length_found = Focal_Length_Finder(
    Known_distance, Known_width, ref_image_face_width)
  
print(Focal_length_found)
  
# mostra a imagem
cv2.imshow("ref_image", ref_image)
  
# inicializa a camera para mostrar o frame
cap = cv2.VideoCapture(0)
if cap.isOpened() is False:
    print("Erro ao encontrar camera")
    ip = input("Digite o Ip da camera: ")
    cap = cv2.VideoCapture('https://'+ip+':8080/video')
  
# ciclo atravez do frame obtido pela camera
while True:
  
    # le o frame da camera
    _, frame = cap.read()
  
    # chama a função para achar o diametro do rosto no frame
    face_width_in_frame = face_data(frame)
  
    # checar para ver se o diametro e diferente de zero 
    if face_width_in_frame != 0:
        
        # acha a distancia chamando a funcao
        # para achar a funcao precisa desses argumentos
        # Focal_Length,
        # Known_width(centimetros),
        # e Known_distance(centimetros)
        Distance = Distance_finder(
            Focal_length_found, Known_width, face_width_in_frame)
  
        # desenha linha como plano de fundo
        cv2.line(frame, (30, 30), (230, 30), RED, 32)
        cv2.line(frame, (30, 30), (230, 30), BLACK, 28)
  
        # Escreve texto no frame
        cv2.putText(
            frame, f"Distance: {round(Distance,2)} CM", (30, 35), 
          fonts, 0.6, GREEN, 2)
  
    # mostra o frame
    cv2.imshow("frame", frame)
  
    # sai se pressionado tecla q
    if cv2.waitKey(1) == ord("q"):
        break
  
# fecha a camera
cap.release()
  
# fecha janelas abertas
cv2.destroyAllWindows()
