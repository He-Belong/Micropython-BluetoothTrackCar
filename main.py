from pyb import delay
from tls01 import TLS01
from MyMotor import bluetooth,Tracking
from MySensor import SensorCheck,HowRun
# 构建蓝牙模块对象（串口）
BLE = TLS01(1, 9600)  # 设置串口号3和波特率,TX--B6,RX--B7

mode='1'#1:表示蓝牙模式 2:循迹模式


mode = 1  # 1: 表示蓝牙模式 2: 循迹模式
def RunMain():
    global mode
    while 1:
        if mode==3:#停机
            break
        if mode==1:#蓝牙
            mode=bluetooth(BLE)
        elif mode==2:#循迹
            mode=Tracking(BLE)
        else:
            pass

def TestSensor():
    global mode
    while 1:
        if mode==3:#停机
            break
        if mode==1:#蓝牙
            mode=bluetooth(BLE)
        elif mode==2:#循迹
            if BLE.uart.any():  # 查询是否有信息
                text = BLE.uart.read(1)  # 默认单次最多接收128字节
                if text.find(b'o')>-1:#停机
                    mode=3
                elif text.find(b'a')>-1:
                    mode=1
            #print(HowRun())
            BLE.uart.write(str(SensorCheck())+'\n')
            print(SensorCheck())
            delay(100)
        else:
            pass
    while 1:
        print(SensorCheck())

RunMain()
#TestSensor()
print('Car Over')
