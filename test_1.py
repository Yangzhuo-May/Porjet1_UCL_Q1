import matplotlib.pyplot as plt
import numpy as np

### données d'exemple
sample_t = np.arange(0., 3., 0.1)
sample_x = 4 * (1 - np.exp(-sample_t))
sample_v = 3 * np.exp(-sample_t)

sample_data = np.array((sample_t, sample_x, sample_v)).T

np.savetxt("sample.data", sample_data)

read_data = np.loadtxt("sample.data")

(t, x, v) = read_data.T

(mesure_t, mesure_x, mesure_v) = np.loadtxt("data/mesure.data").T

plt.figure(1)
plt.subplot(2,1,1)
plt.plot(t, x, label="x sample")
plt.plot(mesure_t, mesure_x, label="x mesure")
plt.legend()
plt.subplot(2,1,2)
plt.plot(t, v, label="v sample")
plt.plot(mesure_t, mesure_v, label="v mesure")
plt.legend()
plt.show()

np.savetxt("sample.csv", sample_data, delimiter=",")
csv_data = np.loadtxt("sample.csv", delimiter=",")