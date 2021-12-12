# 在这里写上你的代码 :-)
'''负责传感器信号的获取和循迹模块的信号获取与判断运动'''
from pyb import ADC
from MyPID import PID
pid=PID(100)
'''6路循迹传感器定义'''
SensorPins = ['X1','X2', 'X3','X4','X5','X6']#
Sensor= [ADC(pin) for pin in SensorPins]
def SensorCheck():
    sensor=[Sensor[p].read() for p in range(len(SensorPins))]
    return sensor

def inrange(s):
    if 800<s<1200:
        return 1
    elif 2900<s<5000:
        return 0
    else:
        return 0

def GetList(sensor):
    aList=[inrange(s) for s in sensor]
    return aList
sensorDict={
0:-2,
1:-1,
2:0,
3:0,
4:1,
5:2
}
Delay10=10
def PIDHowRun():
    sensor=SensorCheck()
    SensorList=GetList(sensor)
    print(SensorList)
    ret=['b',100,100,Delay10]
    if SensorList == [1,1,1, 1,1,1]:
        ret=['g',80,80,Delay10]
    elif SensorList == [0,0,0, 0,0,0]:
        ret=['g',80,80,Delay10]
    else:
        ind=SensorList.index(0)
        rePID=sensorDict[ind]
        speedLR=pid.mypid(rePID)
        ret=['g',speedLR[0],speedLR[1],Delay10]
    print(ret)
    return ret



Kp = 10; Ki = 0.5; Kd = 0;                      #pid弯道参数参数
error = 0; P = 0; I = 0; D = 0; PID_value = 0  #pid直道参数
decide = 0                                     #元素判断
previous_error = 0; previous_I = 0             #误差值
sensor= [0, 0, 0, 0, 0, 0]                      #5个传感器数值的数组
initial_motor_speed = 60;                  #初始速度

def calc_pid(error):
    global P
    global I
    global D
    global PID_value
    global previous_error
    P = error
    I = I + error
    D = error - previous_error
    PID_value = (Kp * P) + (Ki * I) + (Kd * D)
    previous_error = error
    left_motor_speed = initial_motor_speed + PID_value
    right_motor_speed = initial_motor_speed + PID_value
    left_motor_speed=abs(left_motor_speed)
    if(left_motor_speed < 60):
        left_motor_speed = 60
    if(left_motor_speed > 100):
        left_motor_speed = 100
    if(left_motor_speed == None):
        left_motor_speed = 60

    right_motor_speed=abs(right_motor_speed)
    if(right_motor_speed < 60):
        right_motor_speed = 60
    if(right_motor_speed > 100):
        right_motor_speed = 100
    if(right_motor_speed == None):
        right_motor_speed = 60
    return [left_motor_speed,right_motor_speed]

def HowRun():
    sensor=SensorCheck()
    SensorList=GetList(sensor)
    print(SensorList)
    #ret=['b',80,80,50]
    if SensorList == [1,1,1, 1,1,1]:
        ret=['g',95,95,10]
    elif SensorList == [0,0,0, 0,0,0]:
        ret=['g',95,95,10]
    else:
        ind=SensorList.index(0)
        if ind==2 or ind==3:
            ret=['g',90,90,5]
        elif ind==1:
            ret=['m',75,80,3]
        elif ind==0:
            ret=['m',75,80,5]
        elif ind==4:
            ret=['n',80,75,3]
        elif ind==5:
            ret=['n',80,75,5]
        else:
            ret=['g',90,90,5]
    print(ret)
    return ret


def LRG():
    a=SensorCheck()
    print(a)
    if a==[1,1,0,1,1] or a==[1,0,0,0,1]:
        return ['g',50]
    elif a==[1,0,1,1,1] or a==[1,0,0,1,1]:
        return ['l',50]
    elif  a==[0,1,1,1,1] or a==[0,0,1,1,1] or a==[0,0,0,1,1]:
        return ['l',100]
    elif a==[1,1,1,0,1] or a==[1,1,0,0,1]:
        return ['r',50]
    elif a==[1,1,1,1,0] or a==[1,1,1,0,0] or a==[1,1,0,0,0]:
        return ['r',100]
    else:
        return ['g',50]
def CheckRun():
    lrg=LRG()
    print(lrg)
    return lrg
