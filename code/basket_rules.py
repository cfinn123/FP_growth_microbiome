from basket_format import binary_2_basket
import Orange
from orangecontrib.associate.fpgrowth import *

# convert binary data to the basket format
binary_2_basket('../data/test.tab', '../data/output.basket', file_sep='\t')

binary_2_basket('../data/test_airu.tab', '../data/output_airu.basket', file_sep='\t')

table = Orange.data.Table('../data/output.basket')

X, mapping = OneHot.encode(table, include_class=False)

itemsets = dict(frequent_itemsets(X, .95))

rules = association_rules(itemsets, 0.95)

# decode the one.hot encoding
names = {item: '{}={}'.format(var.name, val)
         for item, var, val in OneHot.decode(mapping, table, mapping)}


# write out the results of the rules mined as a text file
with open('../data/test_results.txt', 'w') as f:
    rules = list(rules)
    for ante, cons, supp, conf in rules[:]:
        print(', '.join(names[i] for i in ante), '-->',
              names[next(iter(cons))],
              '(supp: {}, conf: {})'.format(supp, conf), file=f)

