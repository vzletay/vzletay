import cv2
import time
import numpy as np
from djitellopy import Tello

def callback(argument):
    pass

my_font = cv2.FONT_HERSHEY_SIMPLEX
white = (255, 255, 255)
red = (0, 0, 255)
hsv_min = np.array( (18, 56, 149), np.uint8)
hsv_max = np.array((44, 174, 255), np.uint8)
fly = Tello()
fly.connect()
print(fly. get_battery () ) # заряд 'батареи

fly.takeoff()
time.sleep(4)

fly.move_up(185)
fly.rotate_clockwise(45)
fly.move_forward(150)



#окно настройки, слайдеры для настройки фильтра
cv2.namedWindow('Settings')
cv2.createTrackbar('H_min', 'Settings', 34, 36, callback)
cv2.createTrackbar('S_min', 'Settings', 117, 119, callback)
cv2.createTrackbar('V_min', 'Settings', 0, 0, callback)
cv2.createTrackbar('H_max', 'Settings', 196, 198, callback)
cv2.createTrackbar('S_max', 'Settings', 224, 255, callback)
cv2.createTrackbar('V_max', 'Settings', 255, 255, callback)
fly.streamon()
out = cv2.VideoWriter('tello_recording.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (960, 720))
while True:
    frame_read = fly.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.flip(my_frame, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    out.write(my_frame)
#считываем знач ползунков
    h1 = cv2.getTrackbarPos('H_min', "Settings")
    s1 = cv2.getTrackbarPos('S_min', "Settings")
    v1 = cv2.getTrackbarPos('V_min', "Settings")
    h2 = cv2.getTrackbarPos('H_max', "Settings")
    s2 = cv2.getTrackbarPos('S_max', "Settings")
    v2 = cv2.getTrackbarPos('V_max', "Settings")
# формируем нач кон цвет фильтра
    hsv_min = np.array((h1, s1, v1), np.uint8)
    hsv_max = np.array((h2, s2, v2), np.uint8)
# накладываем фильтр на кадр в модели hsv
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)
# моменты изображения - характеристика контура, сумма координат всех пикселей контура
    moments = cv2.moments(thresh, 1)
    dM01 = moments['m01'] # сумма у координат
    dM10 = moments['m10']  # сумма х координат
    dArea = moments['m00'] # колич точек пятна
    if dArea > 1000:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        cv2.circle(thresh, (x, y), 10, (0, 0, 255), -1)
        cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
        text = str(x) + " " + str(y)
        xd = x + 50
        yd = y + 50
        cv2.putText(img, "Find! ", (50, 50), my_font, 1, red,2)
        cv2.putText(img, text, (xd, yd), my_font, 1, red,2)
    cv2.imshow('Result', cv2.resize(thresh, (640, 480)))
    cv2.imshow('Source', cv2.resize(img, (640, 480)))
    cv2.imshow('RGB', cv2.resize(img_rgb,(640, 480)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
fly.rotate_counter_clockwise(90)
fly.move_forward(150)
fly.streamoff()
fly.end()
cv2.destroyAllWindows()