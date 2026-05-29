# БЛОК ИМПОРТА БИБЛИОТЕК
import matplotlib.pyplot as plt  # Импорт библиотеки для базовой визуализации данных

from sklearn.datasets import make_blobs  # Импорт функции для генерации тестовых кластерных данных
import pandas as pd  # Импорт библиотеки для работы с табличными данными

from yellowbrick.cluster import KElbowVisualizer  # Импорт визуализатора для метода локтя
from sklearn.cluster import KMeans  # Импорт алгоритма кластеризации K-средних

import seaborn as sns  # Импорт библиотеки для расширенной статистической визуализации
from collections import Counter  # Импорт инструмента для подсчета количества элементов

# БЛОК ПЕРВОНАЧАЛЬНОГО ТЕСТОВОГО ГРАФИКА (ДО КЛАСТЕРИЗАЦИИ)
zfig, ax = plt.subplots()  # Создание фигуры и осей для графика
ax.plot([1, 2, 3, 4], [1, 4, 2, 5])  # Построение простого линейного графика на тестовых данных
plt.ylabel('Some numbers')  # Подпись оси Y
plt.show()  # Отображение графика на экране
plt.savefig('chart1.png')  # Сохранение графика в файл

# БЛОК ГЕНЕРАЦИИ ДАННЫХ
# make_blobs - функция для создания искусственных кластерных данных
dataset, classes = make_blobs(n_samples=200, n_features=2, centers=4, cluster_std=0.5, random_state=0)
# dataset - координаты точек, classes - истинные метки кластеров
# n_samples=200 - количество точек данных
# n_features=2 - количество признаков (координаты X и Y)
# centers=4 - количество центров кластеров
# cluster_std=0.5 - стандартное отклонение точек внутри кластера
# random_state=0 - фиксация случайности для воспроизводимости результата

df = pd.DataFrame(dataset, columns=['var1', 'var2'])  # Преобразование данных в DataFrame pandas с именами колонок
print(df.head(2))  # Вывод первых двух строк для проверки данных

# БЛОК ОПРЕДЕЛЕНИЯ ОПТИМАЛЬНОГО КОЛИЧЕСТВА КЛАСТЕРОВ (МЕТОД ЛОКТЯ)
model = KMeans(n_clusters=4, random_state=0)  # Инициализация модели KMeans с начальным предположением о 4 кластерах
model._estimator_type = "clusterer"  # Указание типа модели для корректной работы визуализатора
# KElbowVisualizer - инструмент для визуального выбора оптимального k методом локтя
visualizer = KElbowVisualizer(model, k=(1, 12)).fit(df)  # Перебор k от 1 до 12, обучение на данных df
visualizer.show(outpath="chart2.png")  # Отображение графика "локтя" и сохранение в файл

# БЛОК ОБУЧЕНИЯ МОДЕЛИ K-MEANS
# KMeans - реализация алгоритма кластеризации методом K-средних
# init='k-means++' - умный способ инициализации центроидов для улучшения сходимости
kmeans = KMeans(n_clusters=4, init='k-means++', random_state=0).fit(df)  # Обучение модели на данных
# .fit() - основной метод, выполняющий кластеризацию (итеративное уточнение центроидов)

print(kmeans.labels_)  # Вывод предсказанных меток кластеров для каждой точки данных
print(kmeans.cluster_centers_)  # Вывод координат центроидов для каждого кластера
print(kmeans.inertia_)  # Вывод внутрикластерной суммы квадратов (WCSS)
print(kmeans.n_iter_)  # Вывод количества итераций, выполненных алгоритмом

# БЛОК АНАЛИЗА РАЗМЕРОВ КЛАСТЕРОВ
Counter(kmeans.labels_)  # Подсчет количества точек в каждом кластере
print(Counter(kmeans.labels_))  # Вывод размера каждого кластера

# БЛОК ВИЗУАЛИЗАЦИИ КЛАСТЕРОВ (БЕЗ ЦЕНТРОИДОВ)
plt.figure()  # Создание новой фигуры для графика
# sns.scatterplot - построение диаграммы рассеяния с цветовой маркировкой по меткам кластеров
sns.scatterplot(data=df, x='var1', y='var2', hue=kmeans.labels_)
plt.xlabel('var1')  # Подпись оси X
plt.ylabel('var2')  # Подпись оси Y
plt.savefig("chart3.png", dpi=300, bbox_inches="tight")  # Сохранение графика в файл с высоким разрешением
plt.close()  # Закрытие фигуры для освобождения памяти

# БЛОК ВИЗУАЛИЗАЦИИ КЛАСТЕРОВ С ЦЕНТРОИДАМИ
plt.figure()  # Создание новой фигуры
sns.scatterplot(data=df, x='var1', y='var2', hue=kmeans.labels_)  # Отображение точек по кластерам
# plt.scatter - добавление центроидов на график отдельным маркером
# kmeans.cluster_centers_[:,0] - координата X всех центроидов
# kmeans.cluster_centers_[:,1] - координата Y всех центроидов
# marker="X" - форма маркера для центроидов
# c="r" - красный цвет центроидов
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker="X", c="r", s=80, label="centroids")
plt.legend()  # Отображение легенды
plt.xlabel('var1')
plt.ylabel('var2')
plt.savefig("chart4.png", dpi=300, bbox_inches="tight")  # Сохранение финального графика
plt.show()  # Отображение графика на экране
