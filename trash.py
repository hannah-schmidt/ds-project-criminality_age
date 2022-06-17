""""
cur.execute(sql)
    output = cur.fetchall()
    print(output)
    df = pd.DataFrame(cur.fetchall(), columns=['year',
                                               'cases',
                                               'attempts',
                                               'clearanceRate',
                                               'sUnder6',
                                               's6to8',
                                               's8to10',
                                               's10to12',
                                               's12to14',
                                               's14to16',
                                               's16to18',
                                               's18to21',
                                               's21to23',
                                               's23to25',
                                               's25to30',
                                               's30to40',
                                               's40to50',
                                               's50to60',
                                               's60plus'])
"""
#df=read_csv('/Users/hannah/Documents/4-Semester/Data Science/projekt/files/732800.csv')
#print(df.corr())