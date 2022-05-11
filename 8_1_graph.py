import numpy as np
import matplotlib.pyplot as plt

coef = 3.3/255

volt = np.loadtxt ('data.txt')
volt *= coef
settings = np.loadtxt ('settings.txt')

charge = settings[2]
finish = settings[3]
dt = settings[0]
dv = settings[1]

time = np.linspace (0, finish, len(volt))

x_axes = np.linspace (0, finish, 10)
y_axes = np.linspace(0, volt.max(), 10)

plt.ylim([0, volt.max() * 1.1])
plt.xlim([0, finish])

plt.grid()



plt.plot(time, volt, c='blue', linewidth=1, label = 'V(t)')
plt.axvline(charge, linestyle=':', c='black', linewidth=1, label = "start discharging")
    
plt.text(charge + 5, volt.max() - 0.5, "charging time: {:.5f} с".format(charge))
plt.text(charge + 5, volt.max() - 0.6, "discharge time:  {:.5f} с".format(finish - charge))
plt.xlabel(r'$Time$, $c$',    wrap=True)
plt.ylabel(r'Voltage, $V$', wrap=True)
plt.scatter (charge, volt.max(), c="red")

plt.legend()
plt.title('Charging and discharging process in RC circuit', wrap=True)
plt.savefig ('graph.png')
plt.savefig ('graph.svg')