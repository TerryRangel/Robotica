import math as m
import numpy as np
import matplotlib.pyplot as plt


def homog(R, t):
    """Crea matriz homogénea 4x4"""
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = t
    return T

def aplicar(T, p):
    """Aplica transformación homogénea a un punto"""
    p_h = np.append(p, 1)  # [x, y, z, 1]
    return (T @ p_h)[:3]

def inv_homog(T):
    """Inversa de matriz homogénea"""
    R = T[:3, :3]
    t = T[:3, 3]
    T_inv = np.eye(4)
    T_inv[:3, :3] = R.T
    T_inv[:3, 3] = -R.T @ t
    return T_inv

# -------------------------------
# Parte 1: operaciones iniciales
# -------------------------------
print(m.sin(m.pi/2.0))

pB = np.array([1,0,0])
print(pB)
print(pB.shape)

RBA = np.array([[0,-1,0], [0,0,-1], [1,0,0]])
print(RBA)
print(RBA.shape)

tBA = np.array([1,1,1])

# Usar homogéneas en lugar de R@p + t
TBA = homog(RBA, tBA)
pA = aplicar(TBA, pB)
print(pA)
print(pA.shape)

I = np.eye(3)
print(I)

J = np.arange(5,20,3)
print(J)

A = np.zeros((3,2))
print(A)

B = np.ones((3,4))
print(B)

C = np.hstack((A,B))
print(C)

# -------------------------------
# Parte 2: gráfica
# -------------------------------
x = np.linspace(-1, 1, 50)
y = x ** 2
plt.plot(x, y, 'g.-', x, np.sin(x), 'r')
plt.xlabel('valores en x')
plt.ylabel('valores en y')
plt.title('Grafica de x al cuadrado')
# plt.show()  # Puedes activarlo si quieres mostrar

# -------------------------------
# Parte 3: funciones extra
# -------------------------------
def rotx(theta):
    return np.array([[1,0,0],
                     [0,np.cos(theta),-np.sin(theta)],
                     [0,np.sin(theta),np.cos(theta)]])

def roty(theta):
    return np.array([[np.cos(theta),0,np.sin(theta)],
                     [0,1,0],
                     [-np.sin(theta),0,np.cos(theta)]])

def rotz(theta):
    return np.array([[np.cos(theta),-np.sin(theta),0],
                     [np.sin(theta),np.cos(theta),0],
                     [0,0,1]])

# -------------------------------
# Parte 4: transformación inversa
# -------------------------------
TAB = inv_homog(TBA)
RAB = TAB[:3, :3]
tAB = TAB[:3, 3]

print(RAB)
print(tAB)
