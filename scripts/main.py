import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from textwrap import wrap
from collections import namedtuple

SoundDataset = namedtuple('SoundDatset', ['mu', 'Cp', 'Cv']) # создание словаря с табличными значениями

air = SoundDataset(28.97e-3, 1.0036, 0.7166)
water = SoundDataset(18.01e-3, 1.863, 1.403)
co2 = SoundDataset(44.01e-3, 0.838, 0.649)

R = 8.314

with open('conditions.txt', 'r') as f: # считывание измерений из файла
    text = f.readlines()
    humity = float(re.search(r'\d+\.\d+', text[0]).group(0))/100
    Pn = 3170
    temperature = float(re.search(r'\d+\.\d+', text[1]).group(0)) + 273
    xH2O = Pn * humity * water.mu / (R * temperature)

xCO2 = np.linspace(0, 5, 100) / 100 # массив с массовыми долями углекислого газа
xAir = 1 - xCO2 - xH2O # массив с массовыми долями воздуха

Cp = air.mu * air.Cp * xAir + water.mu * water.Cp * xH2O + co2.mu * co2.Cp * xCO2
Cv = air.mu * air.Cv * xAir + water.mu * water.Cv * xH2O + co2.mu * co2.Cv * xCO2

gamma = Cp / Cv # массив с показателями адиабаты
mu = air.mu * xAir + water.mu * xH2O + co2.mu * xCO2 # массив с показателями мю

s_speed = np.sqrt(gamma * R * temperature / mu) # массив со скоростями звука

# for x in xCO2_array:
#
#     Cp = data['N2+O2+Ar'][0] * data['N2+O2+Ar'][1] * xAir + data['H2O'][0] * data['H2O'][1] * xH2O \
#          + data['CO2'][0] * data['CO2'][1] * xCO2
#     Cv = data['N2+O2+Ar'][0] * data['N2+O2+Ar'][2] * xAir + data['H2O'][0] * data['H2O'][2] * xH2O \
#          + data['CO2'][0] * data['CO2'][2] * xCO2
#
#     gamma = Cp / Cv
#
#     Muy = data['N2+O2+Ar'][0] * xAir + data['H2O'][0] * xH2O + data['CO2'][0] * xCO2
#
#     s_speed = math.sqrt(gamma * R * temperature / Muy)
#     sound_speed.append(s_speed)

p = np.polyfit(xCO2, s_speed, 1)

print('Аналитическая формула рассчета скорости звука при заданных температуре и абсолютной влажности:\n'
      'a ≈ {:f} * x + {:f}'.format(p[0], p[1]))

delta_t_air = 3.35 * 10**(-3) # seconds
delta_t_breath = 3.38 * 10**(-3) # seconds
lenth = 1158 * 10**(-3) # meters
speed_air = lenth / delta_t_air # m/s
speed_breath = lenth / delta_t_breath # m/s

n_air = (speed_air - p[1])/p[0] # концентрация углекислого газа для измеренного значения скорости воздуха
n_breath = (speed_breath - p[1])/p[0] # концентрация углекислого газа для измеренного значения скорости углекислого газа

# Построение графика
fig, ax = plt.subplots(figsize=(13, 10), dpi=75)
plt.plot(xCO2 * 100, s_speed, color='b', marker='o', linestyle='-',  linewidth=0.5, markersize=1.5)

plt.rcParams['font.size'] = '14'

title = 'Зависимость скорости звука от концентрации углекислого газа.'
ax.set_title("\n".join(wrap(title, 100)))

plt.xlabel('Концентрация CO$_2$, [%]', fontsize=14)
plt.ylabel('Скорость звука, [м/с]', fontsize=14)

ax.set_xlim(-0.2, 5.2)
ax.set_ylim(min(s_speed) - 0.5, max(s_speed) + 0.5)

ax.minorticks_on()
plt.tick_params(axis='both', which='major', labelsize=14)

ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.2))

ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.2))

ax.grid(which='minor', linewidth='0.5', linestyle='-', color='grey')
ax.grid(which='major', linewidth='1.25', linestyle='-', color='grey')


ax.scatter(n_air * 100, speed_air, color='red', marker='+', s=150, linewidth=2)
ax.scatter(n_breath * 100, speed_breath, color='green', marker='+', s=150, linewidths=2)

plt.legend(['Аналитическая зависимость', 'Значение в воздухе: {:.2f} [м/с], {:.2f} [%]'.format(speed_air, n_air * 100),
            'Значения в выдохе: {:.2f} [м/с], {:.2f} [%]'.format(speed_breath, n_breath * 100)], loc='upper right')

plt.savefig('soundspeed.svg')

plt.show()
