import cv2
import time
import serial
import struct
import threading

#定义命令类型
CMD_LOCK_STATE = 0;
CMD_TEMP_VAL = 1;
CMD_CAP_CTL = 2;
lockstate = "closing"
#串口初始化
UART_NAME = 'COM15'#根据实际串口来修改
ser = serial.Serial(UART_NAME,115200,timeout=1)
#启动摄像头
cap = cv2.VideoCapture(0)

#定义检测到人脸的次数
flag = 0


class Cmd:
    def __init__(self, cap_ctl, temp_val=0.00, lock_state=0):
        self.lock_state = lock_state
        self.temp_val = temp_val
        self.cap_ctl = cap_ctl
    def from_bytes(data):
        cap_ctl, lock_state, temp_val = struct.unpack('<iif', data)
        return Cmd(cap_ctl, round(temp_val,2), lock_state)




#发送指令
def send_cmd(data):
    if ser.is_open:
        send_data = data.encode('utf-8')
        ser.write(send_data)

def serial_rec():
    #读取数据
    #判断串口中是否由数据可读 当有数据可读时 按照结构体(int int float)形式读取串口数据
    if ser.in_waiting > 0:
        d = ser.read(struct.calcsize('iif'))
    #格式化结构体 并实现赋值
        cmd = Cmd.from_bytes(d)
        print(cmd.cap_ctl, cmd.lock_state,cmd.temp_val)
        # 打开线程
        threading.Thread(target=video(cmd), daemon=True).start()
        video(cmd)
    #根据判断效果执行相应内容
    #如果下位机上报的数据是门锁状态 显示到图像界面
    # if cmd.lock_state
    #如果下位机上报的数据是温湿度 显示到人脸识别框的周围
    #如果下位机上报的数据是按下按键 保留当前图像帧为图片




def video(cmd):
    #读取图像 其中ret为是否读到数据 src为读到的数据
    ret,src = cap.read()
    gray=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    mode = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    faces = mode.detectMultiScale(src, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    #如果检测到人脸
    if len(faces) > 0:
        if cmd.lock_state != 1:
            send_cmd("OpenLock")
    #如果没检测到 未检测到一次 闪灯  未检测到五次以上 蜂鸣器响 一秒后关闭
    else:
        global flag
        print("flag = ",flag)
        flag += 1
        if flag == 1:
            send_cmd("F")
        elif flag > 5:
            send_cmd("OpenBuzzer")
            print("已经超过5次未检测到人脸，蜂鸣器已响")
            time.sleep(0.1)
            send_cmd("CloseBuzzer")

    if cmd.cap_ctl == 1:
        lock = threading.Lock()
        with lock:
            last_src = src.copy()
            if last_src is not None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"capture_{timestamp}.jpg"
                cv2.imwrite(filename, last_src, [cv2.IMWRITE_JPEG_QUALITY, 90])
    global lockstate
    if cmd.lock_state:
        lockstate = "opening"
    else:
        lockstate = "closing"
    cv2.putText(src, "The state of lock is "+lockstate+".", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    for (x, y, w, h) in faces:
        cv2.rectangle(src, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(src, "Temp:" + str(cmd.temp_val), (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 0), 2)



    cv2.imshow("input",src)

    #等待一毫秒关闭
    cv2.waitKey(1)

def start_time():
    while True:
        # video()
        serial_rec()
        time.sleep(0.02)

def main():
    start_time()


if __name__=="__main__":
    main()
