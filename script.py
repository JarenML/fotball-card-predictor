import pyautogui
import cv2
import pytesseract
import numpy as np
import time
import datetime
import winsound
from plyer import notification
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Crear carpeta para guardar capturas, de cuando coincide lo que hay en pantall con alguna plantilla
if not os.path.exists("capturas"):
    os.makedirs("capturas")

plantillas = {
    "EMPATE": cv2.imread("imgs/empate.png", cv2.IMREAD_GRAYSCALE),
    "LOCAL": cv2.imread("imgs/local.png", cv2.IMREAD_GRAYSCALE),
    "VISITANTE": cv2.imread("imgs/visitante.png", cv2.IMREAD_GRAYSCALE),
}
print(plantillas["EMPATE"].shape)

orb = cv2.ORB_create()



bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


print("🟢 Iniciando vigilancia... (presionar ctrl+c para terminar)")

while True:
    # captura nueva tomada cada 1 seg. en pantalla
    captura = pyautogui.screenshot()
    captura = cv2.cvtColor(np.array(captura), cv2.COLOR_RGB2BGR)
    zona_resultado = captura[515:600, 940:1320]
    zona_gris = cv2.cvtColor(zona_resultado, cv2.COLOR_BGR2GRAY)

    kp1, des1 = orb.detectAndCompute(zona_gris, None)

    mejor_match = "Desconocido"
    mejor_score = float('inf')

    for nombre, plantilla in plantillas.items():
        kp2, des2 = orb.detectAndCompute(plantilla, None)

        if des1 is not None and des2 is not None:
            matches = bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)
            score = sum([m.distance for m in matches]) / len(matches) if matches else float('inf')

            if score < mejor_score and score < 60:
                mejor_score = score
                mejor_match = nombre

    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Resultado: {mejor_match} (score: {mejor_score:.2f})")

    if mejor_match in ["EMPATE", "LOCAL", "VISITANTE"]:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"capturas/{mejor_match}_{timestamp}.png"
        cv2.imwrite(nombre_archivo, zona_resultado)

        # Sonido de notificación (beep)
        winsound.Beep(1000, 500)  # frecuencia, duración en ms

        # 💬 Notificación emergente
        notification.notify(
            title="Resultado detectado",
            message=f"{mejor_match} detectado. Captura guardada.",
            timeout=5
        )

        print(f"✅ {mejor_match} detectado → Captura guardada como {nombre_archivo}")
        time.sleep(3)  # esperar para evitar duplicados

    time.sleep(1)  # esperar entre chequeos
