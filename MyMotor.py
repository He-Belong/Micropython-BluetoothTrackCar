# 在这里写上你的代码 :-)
from pyb import Pin,Timer,delay
#from MySensor import CheckRun as checkrun
from MySensor import PIDHowRun

#电机端口
M1 = Pin('X7', Pin.OUT)
tim1 = Timer(3, freq=9600) #定时器2设定频率为1600，即每秒输出1600个脉冲数，单位时间内的脉冲数越大，步进电机的速度越快
ch1 = tim1.channel(1, Timer.PWM, pin=M1)  #设定为PWM模式
M2 = Pin('X8', Pin.OUT)
tim2 = Timer(3, freq=9600) #定时器2设定频率为1600，即每秒输出1600个脉冲数，单位时间内的脉冲数越大，步进电机的速度越快
ch2 = tim2.channel(2, Timer.PWM, pin=M2)  #设定为PWM模式
M3 = Pin('Y11', Pin.OUT)
tim3 = Timer(1, freq=9600) #定时器2设定频率为1600，即每秒输出1600个脉冲数，单位时间内的脉冲数越大，步进电机的速度越快
ch3 = tim3.channel(2, Timer.PWM, pin=M3)  #设定为PWM模式
M4 = Pin('Y12', Pin.OUT)
tim4 = Timer(1, freq=9600) #定时器2设定频率为1600，即每秒输出1600个脉冲数，单位时间内的脉冲数越大，步进电机的速度越快
ch4 = tim4.channel(3, Timer.PWM, pin=M4)  #设定为PWM模式

M1.high()
ch1.pulse_width_percent(0)
M2.high()
ch2.pulse_width_percent(0)
M3.high()
ch3.pulse_width_percent(0)
M4.high()
ch4.pulse_width_percent(0)

def Motors(speedL,speedR):
    print('go')
    if speedL>=0:
        ch1.pulse_width_percent(speedL)
        ch2.pulse_width_percent(0)
    else:
        ch1.pulse_width_percent(0)
        ch2.pulse_width_percent(-speedL)
    if speedR>=0:
        ch3.pulse_width_percent(speedR)
        ch4.pulse_width_percent(0)
    else:
        ch3.pulse_width_percent(0)
        ch4.pulse_width_percent(-speedR)
def Go(speed):
    print('go')
    #M1.high()
    ch1.pulse_width_percent(speed)
    #M2.low()
    ch2.pulse_width_percent(0)
    #M3.high()
    ch3.pulse_width_percent(speed)
    #M4.low()
    ch4.pulse_width_percent(0)
def Back(speed):
    print('back')
    #M2.high()
    ch2.pulse_width_percent(speed)
    #M1.low()
    ch1.pulse_width_percent(0)
    #M4.high()
    ch4.pulse_width_percent(speed)
    #M3.low()
    ch3.pulse_width_percent(0)
def TurnRight(speedL,speedR):
    print('right')
    #M1.high()
    ch1.pulse_width_percent(speedL)
    #M2.low()
    ch2.pulse_width_percent(0)
    #M3.low()
    ch3.pulse_width_percent(0)
    #M4.high()
    ch4.pulse_width_percent(speedR)
def TurnLeft(speedL,speedR):
    print('left')
    #M1.low()
    ch1.pulse_width_percent(0)
    #M2.high()
    ch2.pulse_width_percent(speedL)

    #M3.high()
    ch3.pulse_width_percent(speedR)
    #M4.low()
    ch4.pulse_width_percent(0)
'''
def Stop():
    print('stop')
    M1.high()
    ch1.pulse_width_percent(100)
    M2.high()
    ch2.pulse_width_percent(100)
    M3.high()
    ch3.pulse_width_percent(100)
    M4.high()
    ch4.pulse_width_percent(100)
'''
def Stop():
    print('stop')
    #M1.high()
    ch1.pulse_width_percent(100)
    #M2.high()
    ch2.pulse_width_percent(100)
    #M3.high()
    ch3.pulse_width_percent(0)
    #M4.high()
    ch4.pulse_width_percent(0)

#蓝牙部分
def bluetooth(BLE):
    global mode
    print('lanya')
    while 1:
        if BLE.uart.any():  # 查询是否有信息
            text = BLE.uart.read(1)  # 默认单次最多接收128字节
            if text.find(b'o')>-1:#停机
                Stop()
                mode='3'
                return 3
            elif text.find(b's')>-1:
                Stop()
                mode="2"#循迹
                return 2
            elif text.find(b'c')>-1:
                Stop()
            #向前
            elif text.find(b'g')>-1:
                Go(100)
            #后退
            elif text.find(b'b') >-1:
                Back(100)
            #左转
            elif text.find( b'm')>-1:
                TurnLeft(100,100)
            #右转
            elif text.find(b'n')>-1:
                TurnRight(100,100)

'''循迹部分'''
def Tracking(BLE):
    global mode
    global TrackSpeed
    print('Tracking')
    while 1:
        if BLE.uart.any():  # 查询是否有信息
            text = BLE.uart.read(1)  # 默认单次最多接收128字节
            if text.find( b'o')>-1:
                Stop()
                mode='3'
                return 3
            elif text.find(b'a')>-1:
                Stop()
                mode="1"#蓝牙
                return 1
        else:
            #lrgt=checkrun()
            #lrg=lrgt[0]   #取前后循迹模块信号值做出下一步运动的判断
            #RunTime=lrgt[1]   #取前后循迹模块信号值做出下一步运动的判断
            lrg,speedL,speedR,RunTime=PIDHowRun()
            print(speedL,speedR,RunTime)
            #MotorRun(lrg,speedL,speedR,RunTime)
            Motors(speedL,speedR)
            delay(RunTime)

