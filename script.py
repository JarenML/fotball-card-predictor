import pyautogui
import cv2
import pytesseract
import numpy as np

# este es la ruta hacia tessaract, que talvez lo use
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# 1. Cargando imágenes de referencia (plantillas), estas serviran para comparar con las imgns tomadas
plantillas = {
    "EMPATE": cv2.imread("imgs/empate.png", cv2.IMREAD_GRAYSCALE),
    "LOCAL": cv2.imread("imgs/local.png", cv2.IMREAD_GRAYSCALE),
    "VISITANTE": cv2.imread("imgs/visitante.png", cv2.IMREAD_GRAYSCALE),
}

# 2. Capturar pantalla y recortar la zona donde aparece el resultado
captura = pyautogui.screenshot()


# Convertir de PIL a formato OpenCV (de RGB a BGR)
captura = cv2.cvtColor(np.array(captura), cv2.COLOR_RGB2BGR)

# Recortar solo la zona donde aparece el resultado,
zona_resultado = captura[515:600, 940:1320]  

# Convertir a escala de grises para usar con ORB
zona_gris = cv2.cvtColor(zona_resultado, cv2.COLOR_BGR2GRAY)

# -----------------------------
# 3. Procesar con ORB y comparar con las plantillas
# -----------------------------
# Crear detector ORB
orb = cv2.ORB_create()

# Crear matcher de tipo Brute Force con norma de Hamming
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Detectar keypoints y descriptores en la zona capturada
kp1, des1 = orb.detectAndCompute(zona_gris, None)

mejor_match = "Desconocido"
mejor_score = float('inf')

for nombre, plantilla in plantillas.items():
    kp2, des2 = orb.detectAndCompute(plantilla, None)

    if des1 is not None and des2 is not None:
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        print(len(matches))

        # Puntaje promedio de las distancias
        score = sum([m.distance for m in matches]) / len(matches) if matches else float('inf')

        # quedara con el que tenga el score mas bajo, es decir el que mas se parece
        if score < mejor_score:
            mejor_score = score
            mejor_match = nombre

# -----------------------------
# 4. Mostrar resultados
# -----------------------------
print(f"Resultado detectado: {mejor_match} (score: {mejor_score:.2f})")

# Mostrar visualmente la zona comparada
cv2.imshow("Zona detectada", zona_resultado)
cv2.waitKey(0)
cv2.destroyAllWindows()
