# 1задание
# import os
# my_secret = os.environ['Secret_1']
# print(my_secret)

# вывод ключей, работал с Вотинцевой А.С.
# import os

# Secret1_Votintseva = os.environ["Secret1_Votintseva"]
# print(Secret1_Votintseva)

# import os

# Secret2_Votintseva = os.environ["Secret2_Votintseva"]
# print(Secret2_Votintseva)

# import os

# Secret3_Votintseva = os.environ["Secret3_Votintseva"]
# print(Secret3_Votintseva)


# Общее задание, вариант 4, делал с Вотинцевой, проверяла Лысенкова (всё корректно, оценка 5)
from sympy import *

k, T, C, L = symbols("k T C L")
C_ost = 50000
Am_lst = []
C_ost_lst = []
for i in range(9):
    Am = (C - L) / T
    C_ost -= Am.subs({C: 50000, T: 9, L: 0})
    Am_lst.append(round(Am.subs({C: 50000, T: 9, L: 0}), 2))
    C_ost_lst.append(round(C_ost, 2))
print("Am_lst:", Am_lst)
print("C_ost_lst", C_ost_lst)

# 2способ
Aj = 0
C_ost = 50000  # Что это означает? - Это объявление переменной начальной стоимости (Ответ дала Вотинцева А.С.) /Проверил Николаев И.Д., 5/5/
Am_lst_2 = []
C_ost_lst_2 = []
for i in range(9):
    Am = k * 1 / T * (C - Aj)
    C_ost -= Am.subs({C: 50000, T: 9, k: 2})
    Am_lst_2.append(round(Am.subs({C: 50000, T: 9, k: 2}), 2))
    Aj += Am
    C_ost_lst_2.append(round(C_ost, 2))
print("Am_lst_2:", Am_lst_2)
print("C_ost_lst_2", C_ost_lst_2)


# Таблица
import pandas as pd

Y = range(
    1, 11
)  # Что это означает? - Это объявление переменной, которая будет содержать список чисел от 1 до 10 (Ответ дала Вотинцева А.С.) /Проверил Николаев И.Д., 5/5/ /
table1 = list(zip(Y, C_ost_lst, Am_lst))
table2 = list(zip(Y, C_ost_lst_2, Am_lst_2))
tfame = pd.DataFrame(table1, columns=["Y", "C_ost_lst", "Am_lst"])
tfame2 = pd.DataFrame(table2, columns=["Y", "C_ost_lst_2", "Am_lst_2"])
print(tfame)
print(tfame2)

# Визуализация
import numpy as np
import matplotlib.pyplot as plt

plt.figure()
plt.plot(tfame["Y"], tfame["C_ost_lst"], label="Am")
plt.savefig(
    "chart7.png"
)  # Что это означает? - Это сохранение графика в файл (Ответ дала Вотинцева А.С.) /Проверил Николаев И.Д., 5/5/
plt.figure()
plt.plot(tfame2["Y"], tfame2["C_ost_lst_2"], label="Am_2")
plt.savefig("chart8.png")

# Круговые диаграммы 1
vals = Am_lst
labels = [str(x) for x in range(1, 10)]
explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
fig, ax = plt.subplots()
ax.pie(
    vals,
    labels=labels,
    explode=explode,
    autopct="%1.1f%%",
    shadow=True,
    wedgeprops={"lw": 1, "ls": "--", "edgecolor": "k"},
    rotatelabels=True,
)
ax.axis("equal")
plt.savefig("chart9.png")
# Круговые диаграммы 2
vals = Am_lst_2
labels = [str(x) for x in range(1, 10)]
explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
fig, ax = plt.subplots()
ax.pie(
    vals,
    labels=labels,
    explode=explode,
    autopct="%1.1f%%",
    shadow=True,
    wedgeprops={"lw": 1, "ls": "--", "edgecolor": "k"},
    rotatelabels=True,
)
ax.axis("equal")
plt.savefig("chart10.png")

# Гистограммы
table1 = list(zip(Y, Am_lst))
table2 = list(zip(Y, Am_lst_2))
tfame = pd.DataFrame(table1, columns=["Y", "Am_lst"])
tfame2 = pd.DataFrame(table2, columns=["Y", "Am_lst_2"])

plt.figure()
plt.bar(tfame["Y"], tfame["Am_lst"])
plt.savefig("chart11.png")

plt.figure()
plt.bar(tfame2["Y"], tfame2["Am_lst_2"])
plt.savefig("chart12.png")

# Общее задание, вариант 4, делал с Вотинцевой, проверяла Лысенкова (всё корректно, оценка 5)
# Задание 5 Shell
# Задание 6: Поменял исходные данные в соответствии с вариантом 2 ЛР2