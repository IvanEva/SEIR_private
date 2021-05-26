import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


def system(SIRUAP, t, a, b, r, v, g, c, s, w, d, e, S, E, I, R, U, A, P):
    SU, SA, SP, EU, EA, EP, IU, IA, IP, RU, RA, RP = SIRUAP
    I = IU + IA + IP
    return [
        #S
        b + e * (RU) + d * (SP) - (r * I + c * A + w + b) * (SU),
        c * A * (SU) - (s + r * I + b) * (SA),
        w * (SU) + s * (SA) + e * (RP) - (r * I + d + v + b) * (SP),
        #E
        r * I * (SU) - (a + b) * (EU),
        r * I * (SA) - (a + b) * (EA),
        r * I * (SP) - (a + b) * (EP),
        #I
        a * (EU) - (g + b) * (IU),
        a * (EA) - (g + b) * (IA),
        a * (EP) - (g + b) * (IP),
        #R
        g * (IU) + d * (RP) - (e + c * A + w + b) * (RU),
        c * A * (RU) + g * (IA) - (s + b) * (RA),
        w * (RU) + s * (RA) + g * (IP) + v * (SP) - (b + d + e) * (RP)]


t = np.linspace(0, 200, 200)  # vector of time
S = 997 / 1000
E = 0
I = 3 / 1000
R = 0

A = 0
P = 0
U = 1

hard = (906 / 2487) / 10  #https://mosgorzdrav.ru/ru-RU/news/default/card/5642.html
days = 10  #Дни инкубационного периода
maskeff = 0.8  #Коэффициент ношения масок и их эффективности
a = days**(-1) #Инкубационная константа
b = 11.4 / 1000  #Рождаемость(https://ru.wikipedia.org/wiki/%D0%9D%D0%B0%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%8B#%D0%94%D0%B5%D0%BC%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F)
r = 0.4 * (1 - maskeff)  # Заразность
c = 0  #Переход к антивакцинщикам из неопределившихся
g = 0.04  #Вероятность получения иммунитета (переболеть с иммунитетом)
v = 13000 / 12655050  #Вакцинация (по данным Мэрии Москвы в день / официальное население)
e = 1 / (8*30)  #Потеря иммунитета (по исследованиям иммунитет сохраняется приблизительно 5 месяцев)
s = 0  #Переход к пропрививочникам от антипрививочников
w = 0  #Переход к провакцинщикам от неопределившихся
d = 0  #Переход к неопределившимся от провакцинщиков
SIRUAP0 = [S * U, S * A, S * P,E * U, E * A, E * P, I * U, I * A, I * P, R * U, R * A, R * P]  # start value
# b, r, v, g, c, w, s, d, e = map(float, input().split())
w = odeint(system, SIRUAP0, t, args=(a, b, r, v, g, c, w, s, d, e, S, E, I, R, U, A, P))
SU = w[:, 0]
SA = w[:, 1]
SP = w[:, 2]
EU = w[:, 3]
EA = w[:, 4]
EP = w[:, 5]
IU = w[:, 6]
IA = w[:, 7]
IP = w[:, 8]
RU = w[:, 9]
RA = w[:, 10]
RP = w[:, 11]
S = SU + SA + SP
E = EU + EA + EP
I = IU + IA + IP
R = RU + RA + RP

U = SU + EU + IU + RU
A = SA + EA + IA + RA
P = SP + EP + IP + RP
Med = []*len(t)
for i in range(len(t)):
    Med.append(22000/12655050)  #Доля коек для больных Covid19
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=S, name='S'))
fig.add_trace(go.Scatter(x=t, y=E, name='E'))
fig.add_trace(go.Scatter(x=t, y=I, name='I'))
fig.add_trace(go.Scatter(x=t, y=R, name='R'))
fig.add_trace(go.Scatter(x=t, y=hard*I, name='Тяжелые случаи(госпитализация)'))
fig.add_trace(go.Scatter(x=t, y=Med, name='Количество коек'))
fig.update_layout(legend_orientation="h",
                  legend=dict(
                      x=.5,
                      xanchor="center"),
                  xaxis_title="Время в днях",
                  yaxis_title="Доля от популяции",
                  margin=dict(l=0, r=0, t=30, b=0))
fig.update_traces(hoverinfo="all", hovertemplate="Время: %{x}<br>Значение: %{y}")
fig.write_html('first_figure.html', auto_open=True)
