import pandas as pd
import networkx as nx

# Парсинг данных
f1 = open('data-final.csv', 'r')
f2 = open('data-output.csv', 'w')
i = 0
for line in f1:
    arr = line.split('\t')
    # country = arr[107] + '\n'
    arr = arr[:50]
    #arr.append(country)
    arr[49] += '\n'
    f2.write(','.join(arr))
    i += 1
    if i > 3000:
        break

f1.close()
f2.close()

#Отсекающая оценка для коэффициентов корреляции
Correlation_limit = 0.19

# Корреляционные матрицы
data = pd.read_csv('data-output.csv',  engine='python')
corr_all = data.corr()

# Трансформируем в линки для формировнаие ребер:
links = corr_all.stack().reset_index()
links.columns = ['var1', 'var2', 'value']

# Фильтруем ребра по весу (коэф. корреляции) и исключаем loopback
links_filtered=links.loc[ (1 - Correlation_limit > abs(links['value']) > Correlation_limit) & (links['var1'] != links['var2']) ]
links=links_filtered.drop('value', axis=1)

f3 = open('in_graph.txt', 'w')

print(links.to_csv(index=False, sep=' ', header=False, line_terminator='\n'), file=f3)
