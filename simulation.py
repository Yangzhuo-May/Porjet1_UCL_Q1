import numpy as np
import matplotlib.pyplot as plt

#---------définir variables------------
m = 2.0 #kg
g = 9.81 #m/s**2
fd = float(input("entrez un coefficient de frottement : "))

d = 15.0 #m
h_diff = 2.75 #m
h1 = float(input("entrez la hauteur du plus haut point d'ancrage : "))
h2 = h1-h_diff
L = 15.5 #m

h = h2 - h1
f = np.sqrt(d ** 2 + h ** 2)
alpha = np.arctan(h / d)

a = L / 2
b = np.sqrt((L ** 2 - f ** 2) / 4)

#-----tableau temps-----

end = 20
step = 0.01
t = np.arange(0,end,step)

#--------listes de résultats vides-------------
u = np.empty_like(t)
du = np.empty_like(t)
ddu = np.empty_like(t)

v = np.empty_like(t)
dv = np.empty_like(t)
ddv = np.empty_like(t)

#----------conditions initiales--------------
u[0] = -7.57 #calculé via autre code python : calcule u en fct de x (ici x=0)
du[0] = 0

v[0] = 0
dv[0] = 0

#------------calculs------------

for i in range(len(t) - 1):
 dt = step

 v_prime = (b * u[i]) / (a ** 2 * np.sqrt(1 - (u[i] ** 2 / a ** 2)))
 v_second= b / (a ** 2 * np.sqrt((1 - (u[i] ** 2 / a ** 2)) ** 3))

 ddu[i] = (
    - (v_prime * v_second * du[i] ** 2) / ( 1 + v_prime ** 2)
    - (fd * du[i] / m)
    - g * (np.sin(alpha) + v_prime * np.cos(alpha)) / (1 + v_prime ** 2)
 ) #exo 6 annexe H2 dernière ligne

 du[i+1] = du[i] + ddu[i] * dt
 u[i+1] = u[i] + du[i] * dt
 dv[i] = v_prime * du[i]
 ddv[i] = v_second * (du[i] ** 2) + v_prime * ddu[i]

ddu[-1] = ddu[-2]

v = -b * np.sqrt(1 - u**2 / a**2) #exo 3 annexe H2 première ligne

dv[-1] = (
    (b * u[-1]) / (a**2 * np.sqrt(1 - (u[-1] ** 2 / a**2))) * du[-1]
)

ddv[-1] = v_second * (du[-1] ** 2) + v_prime * ddu[-1]

#----------graphiques--------------
plt.figure(figsize=(6, 10))

#trajectoire de la cabine (u en fonction de v)
plt.subplot(4, 1, 1)
plt.plot(u, v, label="Trajectoire ellipse", color="b")
plt.title("Simulation du système de câble")
plt.xlabel("Position u (m)")
plt.ylabel("Altitude v (m)")
plt.legend()

# 2. Vitesses au cours du temps (u et v)
plt.subplot(4, 1, 2)
plt.plot(t, du, label="Vitesse du/dt (m/s)", color="b")
plt.plot(t, dv, label="Vitesse dv/dt (m/s)", color="orange")
plt.title("Vitesses dans les deux directions")
plt.xlabel("Temps (s)")
plt.ylabel("Vitesses (m/s)")
plt.grid(True)
plt.legend()

# 3. Accélérations au cours du temps (u et v)
plt.subplot(4, 1, 3)
plt.plot(t, ddu, label="Accélération ddu (m/s²)", color="b")
plt.plot(t, ddv, label="Accélération ddv (m/s²)", color="r")
plt.title("Accélérations dans les deux directions")
plt.xlabel("Temps (s)")
plt.ylabel("Accélérations (m/s²)")
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(t, u, label="Position u(t)", color="b")
plt.plot(t, v, label="Position v(t)", color="r")
plt.title("Évolution de la position u en fonction du temps")
plt.xlabel("Temps t (s)")
plt.ylabel("Position u (m)")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()

plt.show()