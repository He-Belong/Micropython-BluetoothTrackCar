import pyb
'''
PID使用说明：
    输入参数：当前的编码器值，目标速度对应的编码器值
    输出参数：此时应当的给电机的pwm值
'''
class PID:
    def __init__(self, pwm_range):
        self.pwm_range = pwm_range
        self.II=0
        self.previous_error=0
        self.Kp=40
        self.Ki=0
        self.Kd=45
        self.left_motor_speed =100
        self.right_motor_speed =100

    def mypid(self,error):
        if error==0:
            self.II=0
            self.previous_error=0
            self.left_motor_speed =100
            self.right_motor_speed =100
            return [self.left_motor_speed,self.right_motor_speed]
        P = error
        self.II = self.II + error
        D = error - self.previous_error
        PID_value = (self.Kp * P) + (self.Ki * self.II) + (self.Kd * D)
        print('PID_value:'+str(PID_value))
        self.previous_error = error
        print('previous_error:'+str(self.previous_error))
        self.left_motor_speed = self.left_motor_speed + PID_value
        self.right_motor_speed = self.right_motor_speed - PID_value
        print(self.left_motor_speed,self.right_motor_speed)
        if (self.left_motor_speed >= self.pwm_range):
            self.left_motor_speed = self.pwm_range
        if (self.left_motor_speed <= -self.pwm_range):
            self.left_motor_speed = -self.pwm_range
        if (-40<self.left_motor_speed < 40):
            self.left_motor_speed = 0
        if (self.right_motor_speed >= self.pwm_range):
            self.right_motor_speed = self.pwm_range
        if (self.right_motor_speed <= -self.pwm_range):
            self.right_motor_speed = -self.pwm_range
        if (-40<self.right_motor_speed < 40):
            self.right_motor_speed = 0
        return [self.left_motor_speed,self.right_motor_speed]
