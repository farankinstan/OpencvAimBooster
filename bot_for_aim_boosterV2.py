#только для 1980x1080


#импорт библиотек
import cv2
import numpy as np
import pyautogui as gui
import keyboard
from mss import mss
from time import time


#устанавливаем диапазон цвета
lower = np.array([12, 60, 253])
upper = np.array([179, 62, 255])

#настраиваем данные для счетчика фпс
cTime = 0
pTime = 0

#настраиваем pyautogui
gui.FAILSAFE = False
gui.PAUSE = 0.065


while True:

    #устанавливаем координыты захвата 
    monitor = {"top": 321, "left": 663, "width": 640, "height": 480}

    #производим захват региона экрана
    with mss() as sct:
        video = sct.grab(monitor)

    #превращаем скриншот в массив 
    video = np.array(video)


    #меняем спектр с ргб на хсв
    img = cv2.cvtColor(video, cv2.COLOR_RGB2HSV)  

    #определяем цвет в диапазоне
    mask = cv2.inRange(img, lower, upper) 

    #поиск объекта
    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    #проверяем если есть объекты
    if len(mask_contours) != 0:

        #проходим по всем найденным объектам
        for mask_contour in mask_contours:

            #проверям сколько пикселей в объекте и проверка происходит в диапазоне от 1 и 130
            if cv2.contourArea(mask_contour) > 1 and cv2.contourArea(mask_contour) < 150:

                #получаем и выводим координаты объекта
                x, y, w, h = cv2.boundingRect(mask_contour)
                print(x, y)

                #нажимаем на координаты с учетом , что они на обрезанном кадре
                if not keyboard.is_pressed('q'):
                    gui.click((663 + x) + w // 2, (321 + y) + h // 2)

    #подсчет фпс
    cTime = time()
    fps = 1//(cTime - pTime)
    pTime = cTime

    #вывод фпс
    cv2.putText(video, str(fps), (10,70), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 3)

    #показываем изображение вместе с маской
    cv2.imshow("mask image", mask)

    cv2.imshow("window", video) 

    cv2.waitKey(1)