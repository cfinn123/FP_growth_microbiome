import pandas as pd
import Orange
from orangecontrib.associate.fpgrowth import *

# Read in my relative abundance table which is an m x n dataframe (samples are rows, OTUs are columns.
# File is an output from the program mothur, values are relative abundance values
df = pd.read_csv('../data/test.relabund', sep='\t')

# drop some unwanted columns from the dataframe
df = df.iloc[:, 3:]

# if the relative abundance is above 0.1%, indicate presence with 1 else given 0
df1 = df.where(df <= 0.001, 1)
df1 = df1.where(df >= 0.001, 0)

# Drop rareOTUs as this is actually a combination of OTUs from the mothur filtering stages
df1 = df1.drop('rareOTUs349', axis=1)

# write out the processed data that has been converted, this can be used in the following steps as well as uploaded
# into the Orange GUI to test out and compare
df1.to_csv('../data/test.tab', sep='\t', index=False)

# Steps below are very similar to the documentation provide from Orange

# Read in the tab seperated file created in the previous step as Orange.data.table
table = Orange.data.Table('../data/test.tab')

# Apply one-hot transformation to the data resulting in booleans
X, mapping = OneHot.encode(table, include_class=False)

# Mine items sets from the data, parameters are the one-hot transformed data and a min support cutoff
itemsets = dict(frequent_itemsets(X, .95))

# Obtain rule sets from the itemset, parameters are the itemset previously obtained and a min confidence cutoff
rules = list(association_rules(itemsets, .95))

# decode the one.hot encoding
names = {item: '{}={}'.format(var.name, val)
         for item, var, val in OneHot.decode(mapping, table, mapping)}

# write out the results of the rules mined as a text file
with open('../data/results.txt', 'w') as f:
    for ante, cons, supp, conf in rules[:]:
        supp = supp * 2
        print(', '.join(names[i] for i in ante), '-->',
              names[next(iter(cons))],
              '(supp: {}, conf: {})'.format(supp, conf), file=f)
