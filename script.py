import pyautogui
import cv2
import pytesseract
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


captura = pyautogui.screenshot()


captura = cv2.cvtColor(np.array(captura), cv2.COLOR_RGB2BGR)

zona_resultado = captura[350:850, 830:1430]  #


cv2.imshow("zona_resultado", zona_resultado)
cv2.waitKey(0)
cv2.destroyAllWindows()

