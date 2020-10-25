import pandas as pd
import numpy as np

names = ['test1', 'test2', 'test3', 'test4']
ages = [30, 25, 19, 20]
indexs = [i for i in np.random.randint(0, len(names), 20)]
df = pd.DataFrame({
    'id': [i for i in range(20)],
    'name': [names[x] for x in indexs],
    'age': [ages[x] for x in indexs],
    'order_id': [i for i in np.random.randint(0, 6, 20)]
})

df1 = pd.DataFrame({
    'id': [i for i in range(20)],
    'name': [names[x] for x in indexs]
})

df2 = pd.DataFrame({
    'id': [i for i in range(10)],
    'order_id': [i for i in np.random.randint(1, 20, 10)]
})

# 1. SELECT * FROM data;
df

# 2. SELECT * FROM data LIMIT 10;
df.head(10)

# 3. SELECT id FROM data;  //id 是 data 表的特定一列
df['id']

# 4. SELECT COUNT(id) FROM data;
df['id'].count()

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
df[(df['id'] < 1000) & (df['age'] > 30)]

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
df.groupby('id').size()

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
pd.merge(df1, df2, on='id', how='inner')

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([df1, df2])

# 9. DELETE FROM table1 WHERE id=10;
df1 = df1[df['id'] != 10]

# 10. ALTER TABLE table1 DROP COLUMN column_name;
df1 = df1.drop(columns='name')
