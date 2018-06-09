# FP-growth application to microbiome data

By: **Casey Finnicum**  06/09/18

**Orange3 citation**: Demsar J, Curk T, Erjavec A, Gorup C, Hocevar T, Milutinovic M, Mozina M, Polajnar M, Toplak M, Staric A, Stajdohar M, Umek L, Zagar L, Zbontar J, Zitnik M, Zupan B (2013) Orange: Data Mining Toolbox in Python. Journal of Machine Learning Research 14(Aug):2349−2353.

**This repository shows how to exeute the FP-growth associatice rule mining process using the Orange3 python package**


- The example file `data/test.relabund` is an example relative abundance file that would be output from the mothur software. This file is m x n where m are the samples and n are the various OTUs.


- Execution of `code/FP_growth_0.1.py` will output `results.txt` as well as `test.tab` which can be used to test the similarity of results obtained using the GUI version of Orange3

`results.txt` will contain the results of the mined rules.


