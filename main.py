# import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import numpy as np
from statsmodels.formula.api import ols
import statsmodels.api as sm

url_ = "mysql+pymysql://root:pass@zelophed.duckdns.org:5001/v3"
pop_file = '/Users/hannah/Downloads/01-BU-BV-TVBZ-deu-ab-1987_xls.xlsx'
pop_rtf = "/Users/hannah/Documents/4-Semester/Data Science/projekt/files/crime_keys.rtf"

# read csv file
def read_csv(filename):
    data = pd.read_csv(filename)
    return data

# read population data
def read_pop_file():
    xls = pd.ExcelFile(pop_file)
    pop_count = xls.parse(skiprows=9)
    return pop_count

# connect to database
def dbconnect():
    engine = create_engine(url=url_)
    return engine

# turn absolute numbers into numbers relative to the population
def relativeNumbers(bev, bev_column, df, df_column):
    i = 1993
    while i <= 2021:
        try:
            index, = bev[bev['s2'] == i].index
            pop = bev.at[index, bev_column]
        except:
            pop = bev.at[26, bev_column]

        index, = df.index[df['year'] == i].tolist()
        val = df.at[index, df_column]
        df.at[index, df_column] = (val / pop) * 100000
        i = i + 1
    return df

def convertTuple(tup):
    st = ''.join(map(str, tup))
    return st

def read_crime_keys():
    crime_keys = []
    with open(pop_rtf) as infile:
        for line in infile:
            s = line[1:7]
            crime_keys.append(s)
    del crime_keys[0:10]
    # Summenschlüssel müssen raus, da diese andere Schlüssel
    # miteinschließen und somit das ergebnis verfälschen
    del crime_keys[crime_keys.index('100000')]
    del crime_keys[crime_keys.index('200000')]
    return crime_keys


def read_db_table(table_id, conn):
    # read Population count file
    bev = read_pop_file()
    i = 36
    while i < 130:
        bev.drop(index=[i], inplace=True)
        i = i + 1
    bev = bev.set_axis(
        ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11",
         "s12", "s13", "s14", "s15", "s16", "s17", "s18", "s19", "s20", "s21", "s22"], axis=1)
    cols_y = ['s6', 's7', 's9', 's10', 's12']
    cols_o = ['s14', 's15', 's17']
    bev['s10to21'] = bev[cols_y].sum(axis=1)
    bev['s21to30'] = bev[cols_o].sum(axis=1)
    bev.drop(['s1', 's3', 's4', 's5', 's6', 's7', 's8', 's9',
              's10', 's11', "s12", "s13", "s14", "s15", "s16", "s17"], axis=1, inplace=True)

    # data extraction with SQL statement
    tableNum = convertTuple(("v3.", table_id))
    temp = ('SELECT * FROM ', tableNum)
    sql = convertTuple(temp)
    try:
        df = pd.DataFrame()
        df = pd.read_sql(sql, con=conn)
    except:
        print('error: unable to fetch data')
        conn.close()
    # sum columns to achieve 10 year intervals
    cols_y = ['s10to12', 's12to14', 's14to16', 's16to18', 's18to21']
    cols_o = ['s21to23', 's23to25', 's25to30']
    df['s10to21'] = df[cols_y].sum(axis=1)
    df['s21to30'] = df[cols_o].sum(axis=1)
    df.drop(['sUnder6', 's6to8', 's8to10', 's10to12', 's12to14', 's14to16', 's16to18',
             's18to21', 's21to23', 's23to25', 's25to30', 's60plus'], axis=1, inplace=True)

    # turn absolute numbers into relative numbers
    df = df.sort_values(by='year')
    df = relativeNumbers(bev, 's10to21', df, 's10to21')
    df = relativeNumbers(bev, 's21to30', df, 's21to30')
    df = relativeNumbers(bev, 's18', df, 's30to40')
    df = relativeNumbers(bev, 's19', df, 's40to50')
    df = relativeNumbers(bev, 's20', df, 's50to60')
    # sum every s%to% column
    data = [
        df['s10to21'].sum(),
        df['s21to30'].sum(),
        df['s30to40'].sum(),
        df['s40to50'].sum(),
        df['s50to60'].sum(),
    ]
    return pd.Series(data)


if __name__ == '__main__':
    # Database connection
    engine = dbconnect()
    conn = engine.connect()

    data = {"crime_count": [], "age": []}
    gesamt = pd.DataFrame(data)
    age = [15, 25, 35, 45, 55]  # means of 10 year age intervals

    crime_keys = read_crime_keys()
    for key in crime_keys:
        # allocate age to suspect count
        result = []
        result.append(read_db_table(key, conn).tolist())
        result.append(age)
        temp = pd.DataFrame(result).transpose()
        temp.columns = ['crime_count', "age"]
        gesamt = pd.concat([gesamt, temp])
        if key == "143100":
            sexuelleSelbstbestimmung = gesamt
            gesamt = pd.DataFrame(data)
        if key == "234200":
            rohheitsdelikte_persFreiheit = gesamt
            gesamt = pd.DataFrame(data)
        if key == "375000":
            einfacherDiebstahl = gesamt
            gesamt = pd.DataFrame(data)
        if key == "475000":
            schwererDiebstahl = gesamt
            gesamt = pd.DataFrame(data)
            break
    conn.close()
    crime_categories = [sexuelleSelbstbestimmung, rohheitsdelikte_persFreiheit, einfacherDiebstahl, schwererDiebstahl]

    # Creating a Linear Regression model on the data + plotting + validation
    i = 1
    for category in crime_categories:
        x_data = category['age']
        y_data = category['crime_count']

        # Model 1
        coeffs = np.polyfit(x_data, y_data, 1)
        results = coeffs.tolist()
        print('Model 1 coeffs: ')
        print(results)
        # r-squared
        p = np.poly1d(coeffs) # p = -9.807470833041988x + 752.6087057410723
        # fit values, and mean
        y_vals = p(x_data)
        ybar = np.sum(y_data) / len(y_data)  # Mittelwert von y_data
        SQT = np.sum((y_data - ybar) ** 2)  # summe von (yi - ybar)^2
        SQE = np.sum((y_vals - ybar) ** 2)  # summe von (p(xi) - ybar)^2
        r_squared = SQE / SQT
        print('R squared: ')
        print(r_squared)
        # Model 2 (hat die gleichen Koeffizienten wie Model 1 d.h. die gleiche Regressionsfunktion
        model = ols('crime_count ~ age', data=category).fit()
        coeffs = model.params
        results = coeffs
        # plotting data and linea regression function
        plt.figure(figsize=(8, 8))
        plt.plot(x_data, y_data, 'b.')
        plt.plot(x_data, results[1] * x_data + results[0])
        plt.xlabel("Age (mean)")
        plt.ylabel("Amount suspects per 100.000")
        # Residual Plots for regression model validation
        fig_2 = plt.figure(figsize=(9, 6))
        fig_2 = sm.graphics.plot_regress_exog(model, 'age', fig=fig_2)
    plt.show()
    
    """
    # Plot alle Straftatenschlüssel
    
    data = read_csv("/Users/hannah/Documents/4-Semester/Data Science/projekt/files/crimeCodes.csv")
    data=  pd.DataFrame(data)
    data.drop(data.index[0], inplace=True)

    s10 = pd.DataFrame(data['amount10UpTo21'])
    s10.columns = ['suspects']
    s10['age'] = pd.Series([15 for x in range(len(s10.index))])
    s20 = pd.DataFrame(data['amount21UpTo30'])
    s20.columns = ['suspects']
    s20['age'] = pd.Series([25 for x in range(len(s20.index))])
    s30 = pd.DataFrame(data['amount30UpTo40'])
    s30.columns = ['suspects']
    s30['age'] = pd.Series([35 for x in range(len(s30.index))])
    s40 = pd.DataFrame(data['amount40UpTo50'])
    s40.columns = ['suspects']
    s40['age'] = pd.Series([45 for x in range(len(s40.index))])
    s50 = pd.DataFrame(data['amount50UpTo60'])
    s50.columns = ['suspects']
    s50['age'] = pd.Series([55 for x in range(len(s50.index))])
    data = pd.DataFrame(pd.concat([s10, s20, s30, s40, s50]))

    x_data = data['age']
    y_data = data['suspects']

    model = ols('suspects ~ age', data=data).fit()
    coeffs = model.params
    results = coeffs
    print(results)
    # plotting data and linea regression function
    plt.figure(figsize=(8, 8))
    plt.plot(x_data, y_data, 'b.')
    plt.plot(x_data, results[1] * x_data + results[0])
    plt.xlabel("Age (mean)")
    plt.ylabel("Amount suspects per 100.000")
    # Residual Plots for regression model validation
    fig_2 = plt.figure(figsize=(9, 6))
    fig_2 = sm.graphics.plot_regress_exog(model, 'age', fig=fig_2)

    plt.show()

    """

