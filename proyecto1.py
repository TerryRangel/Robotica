"""
Máquina de estados para evasión de obstáculos
Robótica Móvil - Universidad de Guanajuato
Dr. Juan Pablo I. Ramírez Paredes <jpi.ramirez@ugto.mx>

Este ejemplo implementa un controlador en Python para el 
robot Pioneer 3DX de Adept, utilizando una máquina de estados 
para evadir obstáculos detectados con sensores ultrasónicos.
"""

from controller import Robot, Motor, DistanceSensor
import math as m
import scipy.interpolate as spi
import matplotlib.pyplot as plt


numpoints=9 #seran 9 mas nuestro punto inicial que ese no sera aleatorio

loc = gps.getValues() #obtenemos el lugar inicial de nuestro robot
xarr = np.random.rand(numpoints)*10
yarr = np.random.rand(numpoints)*10

yarr=np.insert(yarr,0,loc[1]) #insertamos la posicion inicial en y
xarr=np.insert(xarr,0,loc[0]) #insertamos la posicion inicial en x

# ------------------------------------------------------------
# 🔹 Función: Conversión de velocidades lineales/angulares a velocidades de rueda
# ------------------------------------------------------------
def velocidad_llantas(vel,vel_angular):
    radio=0.195
    distancia_llantas=0.35
    
    rw= (vel/radio)+((distancia_llantas*vel_angular)/2*radio)
    lw= (vel/radio)-((distancia_llantas*vel_angular)/2*radio)
    
    return rw,lw
    


# ------------------------------------------------------------
# 🔹 Función: Diferencia angular limitada al rango [-pi, pi]
# ------------------------------------------------------------
def diferencia_angular(angulo_1, angulo_2):
    """
    Calcula la diferencia de ángulo (angulo_2 - angulo_1)
    asegurando que el resultado quede entre [-pi, pi]
    """
    magnitud = m.acos(m.cos(angulo_1) * m.cos(angulo_2) + m.sin(angulo_1) * m.sin(angulo_2))
    direccion = m.cos(angulo_1) * m.sin(angulo_2) - m.sin(angulo_1) * m.cos(angulo_2)
    return m.copysign(magnitud, direccion)


# ------------------------------------------------------------
# 🔹 Inicialización del robot y dispositivos
# ------------------------------------------------------------
robot = Robot()
timestep = int(robot.getBasicTimeStep())  # Intervalo de simulación [ms]

# Listas para sensores
sensores_proximidad = []
lectura_sensores = []

# Inicializar los 16 sensores de distancia
for i in range(16):
    sensor = robot.getDevice('so' + str(i))
    sensor.enable(timestep)
    sensores_proximidad.append(sensor)
    lectura_sensores.append(0)

# Motores
leftMotor = robot.getDevice('left wheel')
rightMotor = robot.getDevice('right wheel')
gps = robot.getDevice('gps')
imu = robot.getDevice('inertial unit')
 
gps.enable(timestep)
imu.enable(timestep)
 
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

# ------------------------------------------------------------
# 🔹 Variables del control
# ------------------------------------------------------------
contador_pasos = 0
lista_pos_x = []
lista_pos_y = []
lista_orientacion = []

evadiendo_obstaculo = False
tiempo_inicio = robot.getTime()

# ------------------------------------------------------------
# 🔹 Bucle principal de control
# ------------------------------------------------------------
while robot.step(timestep) != -1:

    tiempo_actual = robot.getTime() - tiempo_inicio

    # Leer sensores de proximidad (valores entre 0 y 5 m)
    for i in range(16):
        valor_sensor = -5.0 * sensores_proximidad[i].getValue() / 1024.0 + 5.0
        if valor_sensor > 1.0 - 1e-8:  # Límite de detección a 1 m
            valor_sensor = None
        lectura_sensores[i] = valor_sensor

    print(lectura_sensores)

    # Detección de obstáculos (izquierda y derecha)
    obstaculo_izquierda = any([lectura_sensores[i] for i in range(0, 4)])
    obstaculo_derecha = any([lectura_sensores[i] for i in range(4, 8)])

    # --------------------------------------------------------
    # 🔸 Máquina de estados para evasión
    # --------------------------------------------------------

    # Estado 1: Avanzar
    if not obstaculo_izquierda and not obstaculo_derecha:
        evadiendo_obstaculo = False
        vel_lineal = 0.3
        vel_angular = 0.0

    # Estado 2: Girar a la derecha
    elif obstaculo_izquierda and not evadiendo_obstaculo:
        evadiendo_obstaculo = True
        print(' Girar a la derecha')
        vel_lineal = 0.0
        vel_angular = -1.0

    # Estado 3: Girar a la izquierda
    elif obstaculo_derecha and not evadiendo_obstaculo:
        evadiendo_obstaculo = True
        print('Girar a la izquierda')
        vel_lineal = 0.0
        vel_angular = 1.0

    # --------------------------------------------------------
    # 🔹 Enviar velocidades a las ruedas
    # --------------------------------------------------------
    rw, lw = velocidad_llantas(vel_lineal, vel_angular)
    leftMotor.setVelocity(lw)
    rightMotor.setVelocity(rw)

    contador_pasos += 1

# ------------------------------------------------------------
# 🔹 Detener el robot al finalizar
# ------------------------------------------------------------
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)
 