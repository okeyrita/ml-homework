# -*- coding: utf-8 -*-
"""lab6-12var

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gQghswqwTmzXnf2R2XgVQh7Z3L-fHg77

lab 6 12 вариант
"""

# импортируем библиотеку
import pandas as pd
# применим функцию read_csv() и посмотрим на первые три записи файла train.csv
train = pd.read_csv('sample_data/train.csv')
train.head(3)

# сделаем то же самое с файлом test.csv
test = pd.read_csv('sample_data/test.csv')
test.head(3)

train.info()

# для построения графиков воспользуемся библиотекой seaborn
import seaborn as sns
# посмотрим насколько значим параметр рэйтинга от даты оценки
# с помощью x и hue мы можем уместить две категориальные переменные на одном графике
sns.countplot(x = 'rating', hue = 'review_date', data = train)

# оценка рейтинга в зависимости от процента содержания какао
sns.countplot(x = 'rating', hue = 'cocoa_percent', data = train)

# выявим пропущенные значения с помощью .isnull() и посчитаем их количество sum()
train.isnull().sum()

# удалим  строки с пустыми значениями в какой то из колонок, так как мы не можем построить на них модель и дать оценку
train.dropna(inplace = True)
# посмотрим на результат
train.isnull().sum()

# применим one-hot encoding к переменной страны компании с помощью метода .get_dummies()
# get_dummies разбивыает более сложные столбцы на бинарные столбцы по каждому параметру
company_location = pd.get_dummies(train['company_location'], dtype='int', prefix = 'location')
company_manufacturer = pd.get_dummies(train['company_manufacturer'], dtype='int')
country_of_bean_origin = pd.get_dummies(train['country_of_bean_origin'], dtype='int', prefix = 'origin')
specific_bean_origin_or_bar_name = pd.get_dummies(train['specific_bean_origin_or_bar_name'], dtype='int', prefix = 'origin_or_bar_name')
ingredients = pd.get_dummies(train['ingredients'], dtype='int')
most_memorable_characteristics = pd.get_dummies(train['most_memorable_characteristics'], dtype='int')
pd.get_dummies(train).head(3)

train = pd.concat(
    [
        train, company_location, company_manufacturer, country_of_bean_origin, specific_bean_origin_or_bar_name,
        ingredients, most_memorable_characteristics
    ], axis = 1)

train.drop(
    [
        'company_location', 'company_manufacturer', 'country_of_bean_origin', 'specific_bean_origin_or_bar_name',
        'ingredients', 'most_memorable_characteristics'
    ], axis = 1, inplace = True)
# удалим столбец номера номера записи , он нам не нужен для исследования
train.drop(
    [
        'ref', 'review_date'
    ], axis = 1, inplace = True)
# переведем проценты в дробное число
train['cocoa_percent'] = train['cocoa_percent'].str.rstrip('%').astype(float) / 100.0
train['rating'] = (train['rating']/3.5).astype(int) # будем считать рейтинг>= 3.5 хорошим (1), а ниже - плохим (0)
train.head(5)

# импортируем класс StandardScaler
from sklearn.preprocessing import StandardScaler
# создадим объект этого класса
scaler = StandardScaler()
# выберем те столбцы, которые мы хотим масштабировать
cols_to_scale = ['cocoa_percent']
scaler.fit(train[cols_to_scale])
train[cols_to_scale] = scaler.transform(train[cols_to_scale])
# рассчитаем среднее арифметическое и СКО для масштабирования данных
# применим их
# посмотрим на результат
train.head(3)

print(train.columns)

#train.columns = train.columns.map(str)
train.columns.map(str)

# поместим в X_train все кроме столбца rating
X_train = train.drop('rating', axis = 1)
# столбец 'rating' станет нашей целевой переменной (y_train)
y_train = train['rating']
X_train.head(3)

# импортируем логистическую регрессию из модуля linear_model библиотеки sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
# создадим объект этого класса и запишем его в переменную model
model = LogisticRegression()
# обучим нашу модель
X_train = pd.get_dummies(X_train)
X_train, X_test, y_train, y_test = train_test_split(
    X_train, y_train, test_size=0.2, random_state=100
)
model.fit(X_train, y_train)

# сделаем предсказание класса на обучающей выборке
y_pred_train = model.predict(X_train)

# построим матрицу ошибок
from sklearn.metrics import confusion_matrix
# передадим ей фактические и прогнозные значения
conf_matrix = confusion_matrix(y_train, y_pred_train)
# преобразуем в датафрейм
conf_matrix_df = pd.DataFrame(conf_matrix)
conf_matrix_df

conf_matrix_labels = pd.DataFrame(conf_matrix, columns = ['прогноз низкий рейтинг', 'прогноз высокий рейтинг'], index = ['Факт низкий рейтинг', 'Факт высокий рейтинг'])
conf_matrix_labels

# рассчитаем метрику accuracy вручную
round((1161+709)/(1161 + 18 + 66 + 709), 3)

# импортируем метрику accuracy из sklearn
from sklearn.metrics import accuracy_score
# так же передадим ей фактические и прогнозные значения
model_accuracy = accuracy_score(y_train, y_pred_train)
# округлим до трех знаков после запятой
round(model_accuracy, 3)

test.info()

import numpy as np
# для начала дадим датасету привычное название X_test
X_test = test

# Для того чтобы наша модель смогла работать с тестовой выборкой нам
# нужно таким же образом обработать и эти данные.

# заполним пропуски в переменных ingredients случайным
possible_values = X_test['ingredients'].dropna().unique()
X_test['ingredients'] = X_test['ingredients'].apply(
    lambda x: x if pd.notnull(x) else np.random.choice(possible_values)
)
# выполним one-hot encoding категориальных переменных
company_location = pd.get_dummies(X_test['company_location'], dtype='int', prefix = 'location')
company_manufacturer = pd.get_dummies(X_test['company_manufacturer'], dtype='int')
country_of_bean_origin = pd.get_dummies(X_test['country_of_bean_origin'], dtype='int', prefix = 'origin')
specific_bean_origin_or_bar_name = pd.get_dummies(X_test['specific_bean_origin_or_bar_name'], dtype='int', prefix = 'origin_or_bar_name')
ingredients = pd.get_dummies(X_test['ingredients'], dtype='int')
most_memorable_characteristics = pd.get_dummies(X_test['most_memorable_characteristics'], dtype='int')
# присоединим новые столбцы к исходному датафрейму
X_test = pd.concat(
    [
        X_test, company_location, company_manufacturer, country_of_bean_origin, specific_bean_origin_or_bar_name,
        ingredients, most_memorable_characteristics
    ], axis = 1)
# удалим столбец номера номера записи , он нам не нужен для исследования
X_test.drop(
    [
        'company_location', 'company_manufacturer', 'country_of_bean_origin', 'specific_bean_origin_or_bar_name',
        'ingredients', 'most_memorable_characteristics'
    ], axis = 1, inplace = True)
X_test.drop(
    [
        'ref', 'review_date'
    ], axis = 1, inplace = True)

# переведем проценты в дробное число
X_test['cocoa_percent'] = X_test['cocoa_percent'].str.rstrip('%').astype(float) / 100.0
X_test['rating'] = (X_test['rating']/3.5).astype(int) # будем считать рейтинг>= 3.5 хорошим (1), а ниже - плохим (0)

# Убедимся, что порядок колонок одинаков
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

#X_test = X_test.drop('rating', axis = 1)
# посмотрим на результат
X_test.head(3)

# применим среднее арифметическое и СКО обучающей выборки для масштабирования тестовых
#данных
from sklearn.preprocessing import StandardScaler
# создадим объект этого класса

scaler.fit(X_test[cols_to_scale])
X_test[cols_to_scale] = scaler.transform(X_test[cols_to_scale])
X_test.head(3)

X_test.columns.map(str)

y_pred_test = model.predict(X_test)

# посмотрим на первые 10 прогнозных значений
y_pred_test[:10]

# возьмем индекс bean_type тестовой выборки
ids = test['ref']
# создадим датафрейм из словаря, в котором
# первая пара ключа и значения - это тип бобовых , вторая - прогноз "на тесте"
result = pd.DataFrame({
    'ref': ids,
    'rating': pd.Series(y_pred_test)
})
# посмотрим, что получилось
result.head(5)

# создадим новый файл result.csv с помощью функции to_csv(), удалив при этом индекс
result.to_csv('result.csv', index = False)
# файл будет сохранен в 'Сессионном хранилище' и, если все пройдет успешно, выведем следующий # текст:
print('Файл успешно сохранился в сессионное хранилище!')

"""Качество модели бинаоной классификации. ROC-кривая"""

from sklearn.metrics import roc_curve, roc_auc_score, auc
import matplotlib.pyplot as plt

# 2. Получаем вероятности принадлежности к классу 1
y_scores = model.predict_proba(X_test)[:, 1]  # только вероятности класса 1

# 3. Строим ROC-кривую
fpr, tpr, thresholds = roc_curve(y_pred_test, y_scores)
roc_auc = auc(fpr, tpr)

# 4. Рисуем
plt.figure()
plt.plot(fpr, tpr, color='blue', lw=2, label='ROC-кривая (AUC = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')  # линия случайного выбора
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC-кривая')
plt.legend(loc='lower right')
plt.grid(True)
plt.show()