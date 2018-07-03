import pandas as pd
import csv


# data should be OTU trable file with 1/0 for absence or presence
def binary_2_basket(input_file, out_name, file_sep=','):
    df1 = pd.read_csv(input_file, sep=file_sep)
    df2 = df1.astype(bool)
    otu_columns_true = []
    for index, row in df2.iterrows():
        true_col_list = [col for col in df2.columns if row[col]]
        otu_columns_true.append(true_col_list)

    with open(out_name, "w") as f:
        writer = csv.writer(f)
        writer.writerows(otu_columns_true)


binary_2_basket('../data/test.tab', '../data/output.basket', file_sep='\t')
