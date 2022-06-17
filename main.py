import pandas as pd
import pymysql
import matplotlib.pyplot as plt

def read_csv(filename):
    data = pd.read_csv(filename)
    return data


def read_pop_file():
    xls = pd.ExcelFile('/Users/hannah/Downloads/01-BU-BV-TVBZ-deu-ab-1987_xls.xlsx')
    pop_count = xls.parse(skiprows=9)
    return pop_count


def dbconnect():
    db = pymysql.connect(host='zelophed.duckdns.org',
                         user='root',
                         password='QiLaSlBTRqYweJiZibMD',
                         database='v3',
                         port=5001)
    return db


def relativeNumbers(bev, bev_column, df, df_column):
    i = 1993
    while (i <= 2021):
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


if __name__ == '__main__':
    # read Population count file
    bev = read_pop_file()
    bev = bev.set_axis(
        ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "s13", "s14", "s15", "s16", "s17",
         "s18", "s19", "s20", "s21", "s22"], axis=1)
    # Database
    db = dbconnect()
    cur = db.cursor()
    # SQL
    sql = "SELECT * FROM v3.734700"
    df = pd.DataFrame()
    try:
        df = pd.read_sql(sql, db)
    except:
        print('error: unable to fetch data')
    db.close()
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

    """
    cols_y = ['s10to12', 's12to14', 's14to16', 's16to18', 's18to21']
    cols_o = ['s21to23', 's23to25', 's25to30']
    df['s10to21'] = df[cols_y].sum(axis=1)
    df['s21to30'] = df[cols_o].sum(axis=1)
    """

    print(df.loc[5])

    """df.drop(['s10to12', 's12to14', 's14to16', 's16to18', 's18to21', 's21to23', 's23to25', 's25to30'],
            axis=1, inplace=True)"""

    # plot
    print(df.corr())
    #df.s30to40.hist()
    #df.boxplot(column=['s10to21', 's21to30'])
    df.plot(x='year',
            y=['s10to12', 's12to14', 's14to16', 's16to18', 's18to21', 's21to23', 's23to25', 's25to30', 's30to40', 's40to50', 's50to60', 's60plus'],
            title='development of criminality in Germany over the years')  # kind='scatter'
    plt.xlabel('Years')
    plt.ylabel('number per 100.000')
    plt.show()

#'s8to10', 's10to12', 's12to14', 's14to16', 's16to18', 's18to21', 's21to23', 's23to25', 's25to30','s30to40', 's40to50', 's50to60', 's60plus'