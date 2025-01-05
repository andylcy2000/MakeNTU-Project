import cv2
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
cnt = 121
while True:
    ret, frame = cap.read()             # 讀取影片的每一幀
    if not ret:
        print("Cannot receive frame")   # 如果讀取錯誤，印出訊息
        break
    img = cv2.medianBlur(frame, 7) 
    # output = cv2.Laplacian(img, -1, 1, 5)
    # cv2.imshow('test', output)     # 如果讀取成功，顯示該幀的畫面
    cv2.imshow('test', frame)
    #store png
    save = "/Users/brianyuan/Desktop/NTU/MakeNTU2024/yolo/outputs/" + str(cnt)+".png"
    print(save)
    cv2.imwrite(save, frame)
    cnt += 1
    if cv2.waitKey(2000) == ord('q'):      # 每一毫秒更新一次，直到按下 q 結束
        break
cap.release()                           # 所有作業都完成後，釋放資源
cv2.destroyAllWindows()                 # 結束所有視窗