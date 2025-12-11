import numpy as np
import matplotlib.pyplot as plt

#ACTIVIDAD 1 : MOVIMIENTO DE CUERPO RIGIDO

'''Alumno: Terry Bryan Rangel'''
'''Peticion del problema'''
'''Considere tres marcos de referencia en el plano (2D): {W} es el mundo, 
{B} es un robot omnidireccional (puede moverse en cualquier dirección y rotar sobre su eje)
y {C} es un sensor ultrasónico.El origen de {B} coincide con el centro de rotación del robot,
y el eje X de {B} apunta hacia el frente del robot. El sensor se encuentra en la parte
frontal derecha del robot, de modo que las coordenadas de su origen expresadas en 
{B} son (0.5, −0.3). El sensor ultrasónico en cuestión apunta hacia la derecha del robot,
por lo que el ángulo entre {B} y {C} es θ=−π/2. Para entender mejor esta situación,
vea el gráfico adjunto (ejercicio.png).Escriba un programa en Python que reciba las
coordenadas de un punto en el marco de referencia {C}, y que imprima las coordenadas
de ese mismo punto en los marcos de referencia {B} y {W}. 
Especifique en alguna variable interna de su programa la posición y el ángulo del robot {B}
 con respecto al mundo {W}, por ejemplo, que el robot esté en el punto (2,2) del marco {W}, 
 con ángulo θ=π/4.'''

'''definicion de nuestra matriz de transformacion homogenea que permite  cambiar de un marco a otro '''
def matriz_transformacion(traslacion_x, traslacion_y, angulo):
 
   
    return np.array([
        [np.cos(angulo), -np.sin(angulo), traslacion_x],
        [np.sin(angulo),  np.cos(angulo), traslacion_y],
        [0,0,1]
    ])

#mueve nuestro punto de referencia a nuestro nuevo marco de referencia
def transformar_punto(matriz_transformacion, punto):

    punto_homogeneo = np.array([punto[0], punto[1], 1])
    punto_transformado = matriz_transformacion @ punto_homogeneo
    return punto_transformado[0:2]  



# definimos nuestrs posición del sensor ultrasónico C respecto al robot B
posicion_sensor_relativa_robot_x = 0.5
posicion_sensor_relativa_robot_y = -0.3
 # el sensor apunta hacia la derecha del robot
angulo_sensor_relativo_robot = -np.pi/2  
matriz_transformacion_sensor_a_robot = matriz_transformacion(
    posicion_sensor_relativa_robot_x,
    posicion_sensor_relativa_robot_y,
    angulo_sensor_relativo_robot
)

#definimos la  posición del robot B respecto al mundo W
posicion_robot_en_mundo_x = 2.0
posicion_robot_en_mundo_y = 2.0
angulo_robot_en_mundo = np.pi/4    # angulo robot a 45°
matriz_transformacion_robot_a_mundo = matriz_transformacion(
    posicion_robot_en_mundo_x,
    posicion_robot_en_mundo_y,
    angulo_robot_en_mundo
)

#Introducimos las coordenadas
coordenada_x_sensor = float(input("Introduce la coordenada X del punto en {C}: "))
coordenada_y_sensor = float(input("Introduce la coordenada Y del punto en {C}: "))
punto_en_sensor = (coordenada_x_sensor, coordenada_y_sensor)

# hacemos la transformacion de C a B (sensor a robot)
punto_en_robot = transformar_punto(
    matriz_transformacion_sensor_a_robot,
    punto_en_sensor
)

# hacemos la tranformacion de C a W (sensor a mundo)
matriz_transformacion_sensor_a_mundo = matriz_transformacion_robot_a_mundo @ matriz_transformacion_sensor_a_robot
punto_en_mundo = transformar_punto(
    matriz_transformacion_sensor_a_mundo,
    punto_en_sensor
)


print("\nResultados:")
print("Punto en {C} (sensor):", punto_en_sensor)
print("Punto en {B} (robot):", punto_en_robot)
print("Punto en {W} (mundo):", punto_en_mundo)





#-------------------------------------------------GRAFICAR------------------------------------------------------------------------------------


fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(0, 5)
ax.set_ylim(0, 5)

# gRAFICAMOS EL MUNDO
ax.quiver(0, 0, 1, 0, angles='xy', scale_units='xy', scale=1, color='black', label="Eje X {W}")
ax.quiver(0, 0, 0, 1, angles='xy', scale_units='xy', scale=1, color='gray', label="Eje Y {W}")

# SE GRAFICA EL  ROBOT
ax.plot(posicion_robot_en_mundo_x, posicion_robot_en_mundo_y, 'ro', label="Robot {B}")
ax.quiver(posicion_robot_en_mundo_x, posicion_robot_en_mundo_y,
          np.cos(angulo_robot_en_mundo), np.sin(angulo_robot_en_mundo),
          angles='xy', scale_units='xy', scale=1, color='red')

# SE GRAFICA EL SENSOR
sensor_en_mundo = transformar_punto(matriz_transformacion_robot_a_mundo, (posicion_sensor_relativa_robot_x, posicion_sensor_relativa_robot_y))
ax.plot(sensor_en_mundo[0], sensor_en_mundo[1], 'bo', label="Sensor {C}")
ax.quiver(sensor_en_mundo[0], sensor_en_mundo[1],
          np.cos(angulo_robot_en_mundo + angulo_sensor_relativo_robot),
          np.sin(angulo_robot_en_mundo + angulo_sensor_relativo_robot),
          angles='xy', scale_units='xy', scale=1, color='blue')

# Punto transformado en {W}
ax.plot(punto_en_mundo[0], punto_en_mundo[1], 'gx', markersize=10, label="Punto en {W}")

ax.legend()
plt.grid(True)
plt.show()