import pandas as pd
import pymysql
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression


def read_csv(filename):
    data = pd.read_csv(filename)
    return data


def read_pop_file():
    xls = pd.ExcelFile('/Users/hannah/Downloads/01-BU-BV-TVBZ-deu-ab-1987_xls.xlsx')
    pop_count = xls.parse(skiprows=9)
    return pop_count


def dbconnect():
    engine = create_engine(url="mysql+pymysql://root:QiLaSlBTRqYweJiZibMD@zelophed.duckdns.org:5001/v3")
    return engine


def relativeNumbers(bev, bev_column, df, df_column):
    i = 1993
    while i <= 2021:
        index = bev[bev['s2'] == i].index.tolist()
        try:
            tmp = bev.at[index[0], bev_column]
        except:
            tmp = bev.at[26, bev_column]
        index, = df.index[df['year'] == i].tolist()
        val = df.at[index, df_column]
        df.at[index, df_column] = (val / tmp) * 100000
        i = i + 1
    return df


def convertTuple(tup):
    st = ''.join(map(str, tup))
    return st


def read_crime_keys():
    crime_keys = []
    with open("/Users/hannah/Documents/4-Semester/Data Science/projekt/files/crime_keys.rtf") as infile:
        for line in infile:
            s = line[1:7]
            crime_keys.append(s)
    del crime_keys[0:10]
    return crime_keys


def read_db_table(table_id, conn):
    # read Population count file
    bev = read_pop_file()
    bev = bev.set_axis(
        ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "s13", "s14", "s15", "s16", "s17",
         "s18", "s19", "s20", "s21", "s22"], axis=1)

    # SQL
    tableNum = convertTuple(("v3.", table_id))
    temp = ('SELECT * FROM ', tableNum)
    sql = convertTuple(temp)
    try:
        df = pd.DataFrame()
        df = pd.read_sql(sql, con=conn)
    except:
        print('error: unable to fetch data')
        conn.close()

    df = df.sort_values(by='year')
    df = relativeNumbers(bev, 's5', df, 's8to10')
    df = relativeNumbers(bev, 's6', df, 's10to12')
    df = relativeNumbers(bev, 's7', df, 's12to14')
    df = relativeNumbers(bev, 's9', df, 's14to16')
    df = relativeNumbers(bev, 's10', df, 's16to18')
    df = relativeNumbers(bev, 's12', df, 's18to21')
    df = relativeNumbers(bev, 's14', df, 's21to23')
    df = relativeNumbers(bev, 's15', df, 's23to25')
    df = relativeNumbers(bev, 's17', df, 's25to30')
    df = relativeNumbers(bev, 's18', df, 's30to40')
    df = relativeNumbers(bev, 's19', df, 's40to50')
    df = relativeNumbers(bev, 's20', df, 's50to60')
    df = relativeNumbers(bev, 's21', df, 's60plus')

    cols_y = ['s10to12', 's12to14', 's14to16', 's16to18', 's18to21']
    cols_o = ['s21to23', 's23to25', 's25to30']
    df['s10to21'] = df[cols_y].sum(axis=1)
    df['s21to30'] = df[cols_o].sum(axis=1)
    df.drop(['s10to12', 's12to14', 's14to16', 's16to18', 's18to21', 's21to23', 's23to25', 's25to30'],
            axis=1, inplace=True)

    # sum every s%to% column
    data = [
        table_id,
        df['s10to21'].sum(),
        df['s21to30'].sum(),
        df['s30to40'].sum(),
        df['s40to50'].sum(),
        df['s50to60'].sum(),
        df['s60plus'].sum()
    ]

    tmp = pd.Series(data)
    return tmp


if __name__ == '__main__':
    engine = dbconnect()
    conn = engine.connect()
    data = {
        "crimeCode": ["crimeCode"],
        "s10to21": ["s10to21"],
        "s21to30": ["s21to30"],
        "s30to40": ["s30to40"],
        "s40to50": ["s40to50"],
        "s50to60": ["s50to60"],
        "s60plus": ["s60plus"],
    }
    gesamt = pd.DataFrame(data)
    crime_keys = read_crime_keys()
    for key in crime_keys:
        result = read_db_table(key, conn)
        gesamt.loc[len(gesamt)] = result.tolist()
        if key == "143100":
            sexuelleSelbstbestimmung = gesamt
            gesamt = pd.DataFrame(data)
            break
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

    print(sexuelleSelbstbestimmung)
    sexuelleSelbstbestimmung = sexuelleSelbstbestimmung.transpose()
    print(sexuelleSelbstbestimmung)


    # Creating a Linear Regression model on our data
    lin = LinearRegression()
    lin.fit(sexuelleSelbstbestimmung['0'], sexuelleSelbstbestimmung['1'])
    # Creating a plot
    ax = sexuelleSelbstbestimmung.plot.scatter(x='0', y='1', alpha=.1)
    ax.plot(sexuelleSelbstbestimmung['0'], lin.predict(sexuelleSelbstbestimmung['0']), c='r')
    plt.show()

    """
    # plot
    print(df.corr())
    print(df.head())

    df.plot.box(column=['s10to21', 's21to30', 's30to40', 's40to50', 's50to60', 's60plus'], figsize=(10, 7))


    df.plot(x='year',
            y=['s10to21', 's21to30', 's30to40', 's40to50', 's50to60', 's60plus'],
            title='development of criminality in Germany over the years')  # kind='scatter'
    plt.xlabel('Years')
    plt.ylabel('number per 100.000')

    plt.show()
    """
# 's8to10', 's10to12', 's12to14', 's14to16', 's16to18', 's18to21', 's21to23', 's23to25', 's25to30','s30to40', 's40to50', 's50to60', 's60plus'
