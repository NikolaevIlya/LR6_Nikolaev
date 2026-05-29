# ==================================================
# БЛОК ИМПОРТА БИБЛИОТЕК
# ==================================================
import matplotlib.pyplot as plt  # Импорт библиотеки для базовой визуализации данных
import numpy as np  # Импорт библиотеки для числовых операций

from sklearn.datasets import make_blobs  # Импорт функции для генерации тестовых кластерных данных
import pandas as pd  # Импорт библиотеки для работы с табличными данными

from yellowbrick.cluster import KElbowVisualizer  # Импорт визуализатора для метода локтя
from sklearn.cluster import KMeans  # Импорт алгоритма кластеризации K-средних

import seaborn as sns  # Импорт библиотеки для расширенной статистической визуализации
from collections import Counter  # Импорт инструмента для подсчета количества элементов

# ==================================================
# БЛОК ГЕНЕРАЦИИ ДАННЫХ С ТРЕМЯ ПАРАМЕТРАМИ
# ==================================================
# Генерация числовых данных: 3 признака
dataset, classes = make_blobs(n_samples=200, n_features=3, centers=4, cluster_std=0.5, random_state=0)

# Первый параметр: диапазон [0.01; 1]
param1 = np.interp(dataset[:, 0], (dataset[:, 0].min(), dataset[:, 0].max()), (0.01, 1))
# Второй параметр: диапазон [1; 300]
param2 = np.interp(dataset[:, 1], (dataset[:, 1].min(), dataset[:, 1].max()), (1, 300))

# Третий параметр: категориальный (города)
city_mapping = {0: 'Самара', 1: 'Тольятти', 2: 'Москва'}
param3 = [city_mapping[int(x % 3)] for x in dataset[:, 2]]

# Создание DataFrame
df = pd.DataFrame({
    'param1': param1,
    'param2': param2,
    'city': param3
})

print("Первые 5 строк сгенерированных данных:")
print(df.head())
print("\nСтатистика по данным:")
print(df.describe(include='all'))

# Сохранение данных в CSV файл
df.to_csv('generated_data.csv', index=False, encoding='utf-8')
print("\nДанные сохранены в файл 'generated_data.csv'")

# ==================================================
# БЛОК ПОДГОТОВКИ ДАННЫХ ДЛЯ КЛАСТЕРИЗАЦИИ
# ==================================================
df_encoded = pd.get_dummies(df, columns=['city'], drop_first=False)

print("\nДанные после One-Hot Encoding:")
print(df_encoded.head())

# Сохранение закодированных данных
df_encoded.to_csv('encoded_data.csv', index=False)
print("Закодированные данные сохранены в 'encoded_data.csv'")

# ==================================================
# БЛОК ОПРЕДЕЛЕНИЯ ОПТИМАЛЬНОГО КОЛИЧЕСТВА КЛАСТЕРОВ (МЕТОД ЛОКТЯ)
# ==================================================
model = KMeans(n_clusters=4, random_state=0)
model._estimator_type = "clusterer"
visualizer = KElbowVisualizer(model, k=(1, 12)).fit(df_encoded)
visualizer.show(outpath="chart_elbow.png")
visualizer.show()
print("\nГрафик метода локтя сохранен в файл 'chart_elbow.png'")

# ==================================================
# БЛОК ОБУЧЕНИЯ МОДЕЛИ K-MEANS
# ==================================================
kmeans = KMeans(n_clusters=4, init='k-means++', random_state=0).fit(df_encoded)

# Сохранение результатов в текстовый файл
with open('clustering_results.txt', 'w', encoding='utf-8') as f:
    f.write("="*50 + "\n")
    f.write("РЕЗУЛЬТАТЫ КЛАСТЕРИЗАЦИИ\n")
    f.write("="*50 + "\n\n")

    f.write("1. Метки кластеров для каждой точки данных (первые 20):\n")
    f.write(str(kmeans.labels_[:20]) + "\n\n")

    f.write("2. Координаты центроидов для каждого кластера:\n")
    for i, centroid in enumerate(kmeans.cluster_centers_):
        f.write(f"   Кластер {i}: {centroid}\n")
    f.write("\n")

    f.write(f"3. Внутрикластерная сумма квадратов (inertia): {kmeans.inertia_:.2f}\n\n")

    f.write(f"4. Количество итераций: {kmeans.n_iter_}\n\n")

    cluster_sizes = Counter(kmeans.labels_)
    f.write("5. Размер каждого кластера:\n")
    for cluster, size in sorted(cluster_sizes.items()):
        f.write(f"   Кластер {cluster}: {size} точек\n")

print("\nРезультаты кластеризации сохранены в 'clustering_results.txt'")

# Вывод в консоль
print("\n" + "="*50)
print("РЕЗУЛЬТАТЫ КЛАСТЕРИЗАЦИИ")
print("="*50)
print(f"\nМетки кластеров (первые 20): {kmeans.labels_[:20]}")
print(f"\nЦентроиды: {kmeans.cluster_centers_}")
print(f"\nВнутрикластерная сумма квадратов: {kmeans.inertia_:.2f}")
print(f"\nКоличество итераций: {kmeans.n_iter_}")
print(f"\nРазмер кластеров: {dict(cluster_sizes)}")

# ==================================================
# БЛОК АНАЛИЗА КЛАСТЕРОВ ПО ГОРОДАМ
# ==================================================
df['cluster'] = kmeans.labels_
city_cluster_dist = pd.crosstab(df['city'], df['cluster'])
print("\nРаспределение городов по кластерам:")
print(city_cluster_dist)

# Сохранение распределения
city_cluster_dist.to_csv('city_cluster_distribution.csv', encoding='utf-8')
print("Распределение городов сохранено в 'city_cluster_distribution.csv'")

# ==================================================
# БЛОК ВИЗУАЛИЗАЦИИ (2D проекция: param1 vs param2)
# ==================================================
plt.figure(figsize=(12, 5))

# График 1: Кластеры без центроидов
plt.subplot(1, 2, 1)
sns.scatterplot(data=df, x='param1', y='param2', hue=kmeans.labels_, palette='Set1')
plt.xlabel('Параметр 1 [0.01; 1]')
plt.ylabel('Параметр 2 [1; 300]')
plt.title('Кластеризация точек (без центроидов)')
plt.legend(title='Кластер')

# График 2: Кластеры с центроидами
plt.subplot(1, 2, 2)
sns.scatterplot(data=df, x='param1', y='param2', hue=kmeans.labels_, palette='Set1')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
            marker="X", c="black", s=200, label="Центроиды")
plt.xlabel('Параметр 1 [0.01; 1]')
plt.ylabel('Параметр 2 [1; 300]')
plt.title('Кластеризация точек (с центроидами)')
plt.legend()

plt.tight_layout()
plt.savefig("chart_clusters_2d.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("График 'chart_clusters_2d.png' сохранен")

# ==================================================
# БЛОК ВИЗУАЛИЗАЦИИ: РАСПРЕДЕЛЕНИЕ ПО КЛАСТЕРАМ И ГОРОДАМ
# ==================================================
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='cluster', hue='city')
plt.xlabel('Номер кластера')
plt.ylabel('Количество точек')
plt.title('Распределение городов по кластерам')
plt.legend(title='Город')
plt.savefig("chart_city_clusters.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("График 'chart_city_clusters.png' сохранен")

# ==================================================
# БЛОК ДОПОЛНИТЕЛЬНОЙ ВИЗУАЛИЗАЦИИ (3D график)
# ==================================================
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(df['param1'], df['param2'], kmeans.labels_, 
                     c=kmeans.labels_, cmap='viridis', s=50)
ax.set_xlabel('Параметр 1 [0.01; 1]')
ax.set_ylabel('Параметр 2 [1; 300]')
ax.set_zlabel('Номер кластера')
ax.set_title('3D Визуализация кластеризации')
plt.colorbar(scatter, label='Кластер')
plt.savefig("chart_3d_clusters.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
print("График 'chart_3d_clusters.png' сохранен")

print("\n" + "="*50)
print("ВСЕ ФАЙЛЫ СОХРАНЕНЫ:")
print("- generated_data.csv - исходные данные")
print("- encoded_data.csv - закодированные данные")
print("- clustering_results.txt - результаты кластеризации")
print("- city_cluster_distribution.csv - распределение городов")
print("- chart_elbow.png - метод локтя")
print("- chart_clusters_2d.png - кластеры в 2D")
print("- chart_city_clusters.png - распределение городов")
print("- chart_3d_clusters.png - 3D визуализация")
print("="*50)