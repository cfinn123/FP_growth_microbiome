import pandas as pd
import Orange
from orangecontrib.associate.fpgrowth import *

# Read in my relative abundance table which is an m x n datframe (samples are rows, OTUs are columns output from
# the program mothur, values are trelavtive abunce values
df = pd.read_csv('../data/test.relabund', sep='\t', index_col='Group')

# drop sonme unwanted columns from the dataframe
df = df.iloc[:, 2:]

# if the relative abundance is above 0.1, indicate presence with 1
df1 = df.where(df <= 0.001, 1)
# if the relative abundance is below 0.1, indicate presence with 0
df1 = df1.where(df1 >= 0.001, 0)
# remove OTUs that have 0 variance
df2 = df1.loc[:, df1.var() != 0.0].astype(int)

# write out the processed data that has been converted, this can be used in the follwoing steps as well as uploaded
# into the Orange GUI to test out and compare
df2.to_csv('../data/test.tab', sep='\t', index=False)

# Steps below are very similar to the documentation provide from Orange

# Read in the tab seperated file created in the previous step as Orange.data.table
table = Orange.data.Table('../data/test.tab')

# Apply one-hot transformation to the data resulting in booleans
X, mapping = OneHot.encode(table, include_class=False)

# Mine items sets from the data, parameters are the one-hot transformed data and a min support cutoff
itemsets = dict(frequent_itemsets(X, .90))

# Obtain rule sets from the itemset, parameters are the itemset previously obtained and a min confidence cutoff
rules = list(association_rules(itemsets, .90))

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
