"""
Trajectory generation based on b-spline curves

Author: Juan-Pablo Ramirez-Paredes <jpi.ramirez@ugto.mx>
Mobile Robotics course, University of Guanajuato (2022)
"""

'''Modificacion/Adaptacion : Terry Bryan Rangrl

 Este programa deberá generar una lista de 10 puntos aleatorios en el plano XY, 
 y debe a continuación calcular una trayectoria suave que pase por todos los puntos
generados (puede usar b-splines). Haga que la trayectoria consista de 200 instantes de tiempo,
 con sus correspondientes coordenadas X y Y. (2025)


'''

import numpy as np
import scipy.interpolate as spi
import matplotlib.pyplot as plt

numpoints = 9#Total de puntos

ttime = 10


#Se generan los puntos al azar 
xarr = np.random.rand(numpoints)*10
yarr = np.random.rand(numpoints)*10

yarr=np.insert(yarr,0,5)
xarr=np.insert(xarr,0,3)

tarr = np.linspace(0, ttime, 10)
  #Se hizo el cambio  de cantidad  de instates de tiempo de 100  a 200
tnew = np.linspace(0, ttime, 200)
#Interpolacion
xc = spi.splrep(tarr, xarr, s=0)
yc = spi.splrep(tarr, yarr, s=0)


#Graficar
plt.figure(1)
xnew = spi.splev(tnew, xc, der=0)
ynew = spi.splev(tnew, yc, der=0)
plt.plot(xnew, ynew)
plt.plot(xarr, yarr, '.')
plt.title('Path')
plt.show()

plt.figure(2)

#Se calcula posicion y velocidad
xdot = spi.splev(tnew, xc, der=1)
ydot = spi.splev(tnew, yc, der=1)

#Graficamos posicion y velocidad
plt.plot(tnew, xnew, 'b', label='x')
plt.plot(tnew, ynew, 'r', label='y')
plt.plot(tnew, xdot, 'c', label='xdot')
plt.plot(tnew, ydot, 'm', label='ydot')
plt.plot(tarr, xarr, '.')
plt.plot(tarr, yarr, '.')
plt.legend()
plt.title('Position and velocity over time')
plt.show()