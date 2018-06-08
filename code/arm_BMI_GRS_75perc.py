import pandas as pd
import numpy as np
import Orange
from orangecontrib.associate.fpgrowth import *

df = pd.read_csv('BMI_GRS_arm_75perc/BMI_GRS_subsampled_75.opti_mcc.relabund', sep='\t', index_col='Group', )
print(df)
df = df.iloc[:, 2:]

# cutoff at 0.5% presence
df1 = df.where(df <= 0.001, 1)
df1 = df1.where(df1 >= 0.001, 0)

df2 = df1.loc[:, df1.var() != 0.0]

bmap = {1: True, 0: False}

df2.to_csv('BMI_GRS_arm_75perc/BMI_GRS_0.001_75.csv')
# print(df2)

table = Orange.data.Table('BMI_GRS_0.001_75.tab')

X, mapping = OneHot.encode(table, include_class=False)

itemsets = dict(frequent_itemsets(X, .95))

rules = association_rules(itemsets, .95)

rules = list(rules)

names = {item: '{}={}'.format(var.name, val)
         for item, var, val in OneHot.decode(mapping, table, mapping)}

with open('out.txt', 'w') as f:
    for ante, cons, supp, conf in rules[:]:
        supp = supp*2
        print(', '.join(names[i] for i in ante), '-->',
              names[next(iter(cons))],
              '(supp: {}, conf: {})'.format(supp, conf), file=f)
