"""
years a: 93 (u6,6-8,8-10), 03 (10-12,12-14,14-18,18-21), 13(21-
years b: 93 (u6,6-8,8-10), 03 (10-12,12-14,14-18,18-21), 13(21-
"""

import pandas as pd
import matplotlib.pyplot as plt

def read_csv(filename):
    df = pd.read_csv(filename)
    return df
    #print(df.to_string())

def gens():
    gen_a93 = df.loc[(df['year'] == 1993)].sUnder6 + df.loc[(df['year'] == 1993)].s6to8 + df.loc[(df['year'] == 1993)].s8to10
    gen_a03 = df.loc[(df['year'] == 2003)].s10to12 + df.loc[(df['year'] == 2003)].s12to14 + df.loc[(df['year'] == 2003)].s14to16 + df.loc[(df['year'] == 2003)].s16to18 + df.loc[(df['year'] == 2003)].s18to21
    gen_a13 = df.loc[(df['year'] == 2013)].s21to23 + df.loc[(df['year'] == 2013)].s23to25 + df.loc[(df['year'] == 2013)].s25to30

    gen_b93 = df.loc[(df['year'] == 1993)].sUnder6 + df.loc[(df['year'] == 1993)].s6to8 + df.loc[(df['year'] == 1993)].s8to10
    gen_b03 = df.loc[(df['year'] == 2003)].s10to12 + df.loc[(df['year'] == 2003)].s12to14 + df.loc[(df['year'] == 2003)].s14to16 + df.loc[(df['year'] == 2003)].s16to18 + df.loc[(df['year'] == 2003)].s18to21
    gen_b13 = df.loc[(df['year'] == 2013)].s21to23 + df.loc[(df['year'] == 2013)].s23to25 + df.loc[(df['year'] == 2013)].s25to30

    gen_a = {
        "year": [1993, 2003, 2013],
        "tv": [gen_a93, gen_a03, gen_a13]
    }
    gen_a = pd.DataFrame(gen_a)
    gen_a.plot(kind='scatter', x='year', y='tv')
    plt.show()

def compare():
    zero93 = df.loc[(df['year'] == 1993)].sUnder6 + df.loc[(df['year'] == 1993)].s6to8 + df.loc[(df['year'] == 1993)].s8to10
    zero03 = df.loc[(df['year'] == 2003)].sUnder6 + df.loc[(df['year'] == 2003)].s6to8 + df.loc[(df['year'] == 2003)].s8to10
    zero13 = df.loc[(df['year'] == 2013)].sUnder6 + df.loc[(df['year'] == 2013)].s6to8 + df.loc[(df['year'] == 2013)].s8to10
    zeroten = {
        "year": [1993, 2003, 2013],
        "tv": [gen_a93, gen_a03, gen_a13]
    }

if __name__ == '__main__':
    df=read_csv('/Users/hannah/Documents/4-Semester/Data Science/projekt/files/000000.csv')
    #print(pd.options.display.max_rows)
    #print(df.corr())
    #df.plot(kind='scatter', x='year', y='s18to21')
    #df.plot()
    #plt.show()
    #print(df.sUnder6, df.s6to8)
    gens()
