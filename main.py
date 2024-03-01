import machine, utime, _thread
from machine import Pin

left_sensor = machine.ADC(2)
middle_sensor = machine.ADC(1)
right_sensor = machine.ADC(0)
R_motor_forw = machine.PWM(machine.Pin(3))
R_motor_forw.freq(1000)
R_motor_back = machine.PWM(machine.Pin(4))
R_motor_back.freq(1000)
L_motor_forw = machine.PWM(machine.Pin(1))
L_motor_forw.freq(1000)
L_motor_back = machine.PWM(machine.Pin(2))
L_motor_back.freq(1000)
led = Pin("LED", Pin.OUT)
speed=65000
 
backspeed = int(speed*0.3)
R_motor_back.duty_u16(0) 
L_motor_back.duty_u16(0)
 
def forward ():
    L_motor_forw.duty_u16(speed)    
    R_motor_forw.duty_u16(speed)
 
def stop ():
    L_motor_forw.duty_u16(0)
    R_motor_forw.duty_u16(0)

def right_turn ():
    L_motor_forw.duty_u16(speed)
    R_motor_forw.duty_u16(backspeed)
def left_turn ():
    L_motor_forw.duty_u16(backspeed)
    R_motor_forw.duty_u16(speed)
 
 
global start_pressed
start_pressed = 0
def start_reader_thread():
    global start_pressed
    start = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_DOWN)
    while True:
        utime.sleep(0.1)
        if start.value() == 0:
            if start_pressed == 0:
                start_pressed = 1
#               print("Knapp True")
                utime.sleep(2)
            elif start_pressed == 1:
                start_pressed = 0
#                print("Knapp False")
                utime.sleep(2)
 
_thread.start_new_thread(start_reader_thread, ())
sensor_limit = 20000
while True:
    if start_pressed == 1:
        left_sens = left_sensor.read_u16()
        middle_sens = middle_sensor.read_u16()
        right_sens = right_sensor.read_u16()
#         utime.sleep(0.01)
#         led.value(1)
#         print(left_sens, middle_sens, right_sens)
 
        if ((left_sens < sensor_limit) and (middle_sens > sensor_limit) and (right_sens < sensor_limit)):
            forward()

        elif ((left_sens < sensor_limit) and (right_sens > sensor_limit)):
            right_turn() 

        elif ((left_sens > sensor_limit) and (right_sens < sensor_limit)):
            left_turn()

#         elif ((left_sens < sensor_limit) and (middle_sens < sensor_limit) and (right_sens < sensor_limit)):
#             backward()
            
        elif ((left_sens > sensor_limit) and (middle_sens > sensor_limit) and (right_sens > sensor_limit)):
              stop()
    elif start_pressed == 0:
        stop()
        utime.sleep(0.05)
        led.value(0)