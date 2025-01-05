from ultralytics import YOLO
import cv2
import numpy as np
import sympy as sp
import threading
import time
import sys
import serial

class bluetooth:
    def __init__(self, port: str, baudrate: int=9600):
        """ Initialize an BT object, and auto-connect it. """
        # The port name is the name shown in control panel
        # And the baudrate is the communication setting, default value of HC-05 is 9600.
        self.ser = serial.Serial(port, baudrate=baudrate)
        
    def is_open(self) -> bool:
        return self.ser.is_open

    def waiting(self) -> bool:
        return self.ser.in_waiting

    def do_connect(self, port: str, baudrate: int=9600) -> bool:
        """ Connect to the specify port with particular baudrate """
        # Connection function. Disconnect the previous communication, specify a new one.
        self.disconnect()

        try:
            self.ser = serial.Serial(port, baudrate=baudrate)
            return True
        except:
            return False

    def disconnect(self):
        """ Close the connection. """
        self.ser.close()

    def write(self, output: str):
        # Write the byte to the output buffer, encoded by utf-8.
        send = output.encode("utf-8")
        self.ser.write(send)

    def readString(self) -> str:
        # Scan the input buffer until meet a '\n'. return none if doesn't exist.
        if(self.waiting()):
            receiveMsg = self.ser.readline().decode("utf-8")[:-1]

        return receiveMsg

def read():
    while True:
        if bt.waiting():
            print(bt.readString())

def write():
    while True:
        msgWrite = input()
        
        if msgWrite == "exit": sys.exit()
    
        bt.write(msgWrite + "\n")


_x, _y = sp.symbols('_x _y')
_x1 = 0
_y1 = 0
_x2 = 325
_y2 = 0
_x3 = 0
_y3 = 475
_x4 = 325
_y4 = 475
x1 = 0.42
y1 = 0.65
x2 = 0.4169
y2 = 0.3292
x3 = 0.7708
y3 = 0.6336
x4 = 0.7671
y4 = 0.3141
A = np.zeros((8,8))
A[0][0] = _x1
A[0][1] = _y1
A[0][2] = _x1*_y1
A[0][3] = 1
A[1][0] = _x2
A[1][1] = _y2
A[1][2] = _x2*_y2
A[1][3] = 1
A[2][0] = _x3
A[2][1] = _y3
A[2][2] = _x3*_y3
A[2][3] = 1
A[3][0] = _x4
A[3][1] = _y4
A[3][2] = _x4*_y4
A[3][3] = 1
A[4][4] = _x1
A[4][5] = _y1
A[4][6] = _x1*_y1
A[4][7] = 1
A[5][4] = _x2
A[5][5] = _y2
A[5][6] = _x2*_y2
A[5][7] = 1
A[6][4] = _x3
A[6][5] = _y3
A[6][6] = _x3*_y3
A[6][7] = 1
A[7][4] = _x4
A[7][5] = _y4
A[7][6] = _x4*_y4
A[7][7] = 1
b = np.zeros((8,1))
b[0][0] = x1
b[1][0] = x2
b[2][0] = x3
b[3][0] = x4
b[4][0] = y1
b[5][0] = y2
b[6][0] = y3
b[7][0] = y4
x = np.matmul(np.linalg.inv(A), b)
print(x)
outputx = 0
outputy = 0

model = YOLO('yolov8n.pt')

bt = bluetooth("/dev/tty.HC-05")
while (bt == None):
    bt = bluetooth("/dev/tty.HC-05")
print("BT Connected!")
# result = model.train(data = 'coco8.yaml', epochs = 2, imgsz = 640)
# Solve the equations
# model.train("./contents/data/data.yaml", epcohs=10)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
mov = False
while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame")   # 如果讀取錯誤，印出訊息
        break
    if cv2.waitKey(1000) == ord('q'):      # 每一毫秒更新一次，直到按下 q 結束
        break
    # cv2.imshow('test', frame)
    results = model.predict(frame)
    for r in results:
        r.save("output.png")
        cv2.imshow('test', cv2.imread("output.png"))
        print(r.boxes.cls.numpy())
        idx = np.where(r.boxes.cls.numpy() == 67)
        pos = r.boxes.xyxyn.numpy()[idx]
            
        if len(pos) > 0:
            x1, y1, x2, y2 = r.boxes.xyxyn.numpy()[idx][0]
            print(x1, y1, x2, y2)
            now_x = (x1+x2)/2
            now_y = (y1+y2)/2
            print("x = ", (x1+x2)/2, "y = ", (y1+y2)/2)
            eq1 = sp.Eq(x[0][0]*_x + x[1][0]*_y + x[2][0]*_x*_y + x[3][0], now_x)
            eq2 = sp.Eq(x[4][0]*_x + x[5][0]*_y + x[6][0]*_x*_y + x[7][0], now_y)
            solution = sp.solve((eq1, eq2), (_x, _y))
            # print("Solution:")
            print("_x =", solution[0])
            print("_y =", solution[1])
            posx = round(solution[0][0])
            posy = round(solution[0][1])
            if (abs(posx - outputx) > 3 and abs(posy - outputy) > 3):
                print("move")
                mov = True
                outputx = posx
                outputy = posy
                if (outputx > 325):
                    outputx = 325
                if (outputx < 0):
                    outputx = 0
                if (outputy > 475):
                    outputy = 475
                if (outputy < 0):
                    outputy = 0
        print("posx = ", outputx, "posy = ", outputy)
        if(outputx < 10):
            outstrx = "00" + str(outputx)
        elif(outputx < 100):
            outstrx = "0" + str(outputx)
        else:
            outstrx = str(outputx)
        if(outputy < 10):
            outstry = "00" + str(outputy)
        elif(outputy < 100):
            outstry = "0" + str(outputy)
        else:
            outstry = str(outputy)
        msgWrite = 'a' + outstrx + outstry + 'b'
        if (len(msgWrite) != 8):
            print("error")
            continue
        print(msgWrite)
        if (mov):
            bt.write(msgWrite)
            mov = False

        # for i in range(len(pos)):
        #     x1, y1, x2, y2 = r.boxes.xyxyn.numpy()[idx][i]
        #     now_x = (x1+x2)/2
        #     now_y = (y1+y2)/2
        #     eq1 = sp.Eq(x[0][0]*_x + x[1][0]*_y + x[2][0]*_x*_y + x[3][0], now_x)
        #     eq2 = sp.Eq(x[4][0]*_x + x[5][0]*_y + x[6][0]*_x*_y + x[7][0], now_y)
        #     solution = sp.solve((eq1, eq2), (_x, _y))
        #     posx = round(solution[1][0])
        #     posy = round(solution[1][1])

    # for r in results:
    #     r.save("output.png")
    #     cv2.imshow('test', cv2.imread("output.png"))
    #     # if (r.boxes.cls.numpy() == 0) :
    #     #     print("cell phone detected")
    #     # idx = np.where(r.boxes.cls.numpy() == 0)
    #     # print(idx)
    #     pos = r.boxes.xyxyn.numpy()[idx]
    #     print(pos)
    #     if len(pos) > 0:
    #         print("cell phone detected")
    #         x1, y1, x2, y2 = r.boxes.xyxyn.numpy()[idx][0]
    #         print(x1, y1, x2, y2)
            
    #     # print(type(r.boxes.xyxyn.numpy()))
    #     # print(r.boxes.cls)
    # # print(results[0].names)
    # # for r in results:
    #     # print(r.boxes.cls)
    #     # cls 67 is the class of cell phone
    #     # print(type(r.boxes.cls.numpy()))
    #     # idx = np.where(r.boxes.cls.numpy() == 67)
    #     # x1, y1, x2, y2 = r.boxes.xyxyn.numpy()[idx]
    #     # print(x1, y1, x2, y2)
    #     # print(r.boxes.xyxyn[idx])
    #     # for num in r.boxes.cls:
    #     #     if num == 67:
    #     #         print("cell phone detected")
    #     #         print(r.boxes.xyxyn)