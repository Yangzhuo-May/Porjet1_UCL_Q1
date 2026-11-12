import numpy as np
import matplotlib.pyplot as plt

#---------définir variables------------

m=2.0 #kg
g = 9.81 #m/s**2
fd = float(input("entrez un coefficient de frottement : "))

d=15.0 #m
h = 2.75 #m
h1 = float(input("entrez la hauteur du plus haut point d'ancrage : "))
h2 = h1-h
L = 15.5 #m 绳长，为什么给了确定值？
f = np.sqrt(d**2 + h**2) # 两边端点之间的距离
alpha = np.arctan((h2 - h1) / d) # 绳索与水平距离形成的角度

a = L / 2
b = np.sqrt((L**2 - f**2) / 4)

#-----tableau temps-----
end = 20
step = 0.01
t=np.arange(0,end,step) # 把整段时间切分成每份0.01秒的小份，这是所有小份的容器（列表）

#--------listes de résultats vides-------------

u = np.full_like(t, np.nan)
v = np.full_like(t, np.nan)

du = np.empty_like(t)
dv = np.empty_like(t)

ddu = np.empty_like(t)
ddv = np.empty_like(t)

# ----------conditions initiales--------------
u[0] = -7.5  # calculé via autre code python
v[0] = 0
du[0] = 0
dv[0] = 0

# 计算初始状态并打印（移到循环外面）
u0 = u[0]
vp0 = (b * u0) / (a**2 * np.sqrt(1 - u0**2 / a**2))
vpp0 = b / (a**2 * np.sqrt((1 - u0**2 / a**2)**3))
acc0 = (
    -(vp0 * vpp0 * du[0] ** 2) / (1 + vp0**2)
    - (fd * du[0] / m)
    - g * (np.sin(alpha) + vp0 * np.cos(alpha)) / (1 + vp0**2)
)

print("alpha =", alpha)
print("fd =", fd)
print("u0 =", u0)
print("v_prime =", vp0)
print("v_second =", vpp0)

# ------------calculs------------
for i in range(len(t) - 1):
  if abs(u[i]) >= a:
    print("Erreur à l'itération :", i)
    print("Temps :", t[i])
    print("Position u :", u[i])
    print("Vitesse du :", du[i])
    break

  dt = step

  v_prime = (b * u[i]) / (a**2 * np.sqrt(1 - (u[i] ** 2 / a**2)))  # 一阶导数
  v_second = b / (
      a**2 * np.sqrt((1 - (u[i] ** 2 / a**2)) ** 3)
  )  # 二阶导数

  ddu[i] = (
      -(v_prime * v_second * du[i] ** 2) / (1 + v_prime**2)
      - (fd * du[i] / m)
      - g * (np.sin(alpha) + v_prime * np.cos(alpha)) / (1 + v_prime**2)
  )

  du[i + 1] = du[i] + ddu[i] * dt
  u[i + 1] = u[i] + du[i] * dt
  dv[i] = v_prime * du[i]
  ddv[i] = v_second * (du[i] ** 2) + v_prime * ddu[i]

# v = -b * np.sqrt(1 - u**2 / a**2) #exo 3 annexe H2 première ligne
dv[-1] = (
    (b * u[-1]) / (a**2 * np.sqrt(1 - (u[-1] ** 2 / a**2))) * du[-1]
)

ddv[-1] = v_second * (du[-1] ** 2) + v_prime * ddu[-1]

#----------graphiques--------------

# plt.figure(figsize=(10, 6))
plt.figure(figsize=(10, 10))


#trajectoire de la cabine (u en fonction de v)
# plt.subplot(2, 1, 1)
plt.subplot(4, 1, 1)
plt.plot(u, v, label="Trajectoire ellipse", color="b")
plt.title("Simulation du système de câble")
plt.xlabel("Position u (m)")
plt.ylabel("Altitude v (m)")
plt.grid(True) # added
plt.legend()

# #position u au cours du temps
# plt.subplot(2, 1, 2)
# plt.plot(t, u, label="Position u(t)", color="b")
# plt.plot(t, v, label="Position v(t)", color="y")
# plt.xlabel("Temps (s)")
# plt.ylabel("Positions (m)")
# plt.legend()

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
plt.plot(t, u, label="u")
plt.plot(t, v, label="v")
plt.xlabel("t [s]")
plt.ylabel("u, v [m]")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()