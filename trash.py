"""

        model = linear_model.LinearRegression().fit(x_data, y_data)
           print('score:')
           print(model.score(x_data, y_data))
           print('Intercept: \n', model.intercept_)
           print('Coefficients: \n', model.coef_)

           #alpha, beta = optimize.curve_fit(func, xdata=x_data, ydata=y_data)[0]
           #print(f'alpha={alpha}, beta={beta}')

           X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, test_size=1 / 3, random_state=42)

           X_train = X_train.values.reshape(-1, 1)
           X_test = X_test.values.reshape(-1, 1)

           regressor = LinearRegression()
           regressor.fit(X_train, y_train)
           # Predicting the Test set results
           y_pred = regressor.predict(X_test)
           print('Coefficients: \n', regressor.coef_)
           # The mean squared error
           print("Mean squared error: %.2f" % np.mean((regressor.predict(X_test) - y_test) ** 2))
           # Explained variance score: 1 is perfect prediction
           print('Variance score: %.2f' % regressor.score(X_test, y_test))

           # obtain m (slope) and b(intercept) of linear regression line
           model = linear_model.LinearRegression().fit(x_data, y_data)
           print('score:')
           print(model.score(x_data, y_data))

         # define a function for fitting
        def func(x, a,b):
            y = a * np.exp(-b * x) + d
            return y

        a = 4000
        b = 200
        d = 0
        # y = 11861.83704388 - 2993.99937809 * math.log(X)
        # y = 77551.68653764 - 19517.66772156 * ln(x)
        # y = 55.0002083 - 13.06136124 * ln(x)
        # y = 40.45750785 - 9.85511479 * ln(x)

        plt.scatter(x_data, y_data, color='red', label='data')
        plt.plot(x_data, func(x_data, 4000, 200), color='green', label='model')

        popt, pcov = curve_fit(func, x_data, y_data, bounds=([15, 55]))
        print(popt)
        perr = np.sqrt(np.diag(pcov))
        print(perr)

        model = linear_model.LinearRegression().fit(X, y)
        print('score:')
        print(model.score(X, y))
        print('Intercept: \n', model.intercept_)
        print('Coefficients: \n', model.coef_)



    #X = sexuelleSelbstbestimmung[["10to21", "21to30", "30to40", "40to50", "50to60"]]
    X = merged.drop('crime_count', axis='columns')
    y = merged.crime_count


    print(df.corr())
    print(df.head())

    df.plot.box(column=['s10to21', 's21to30', 's30to40', 's40to50', 's50to60', 's60plus'], figsize=(10, 7))


    df.plot(x='year',
            y=['s10to21', 's21to30', 's30to40', 's40to50', 's50to60', 's60plus'],
            title='development of criminality in Germany over the years')  # kind='scatter'
    plt.xlabel('Years')
    plt.ylabel('number per 100.000')

    plt.show()





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

"""

    #sns.residplot(x=x_data, y=y_data, color='black')

        fig_1 = plt.figure(figsize=(9, 6))
        plt.plot(x_data, y_data, 'b.')
        #plt.scatter(x_data, y_data)

        y = results[1] * x_data + results[0]
        plt.plot(y, 'r')

        plt.xlabel("Age")
        plt.ylabel("Amount of crimes committed per 100.000")
        #abline_plot(model_results=model.fit())
        
        
           # Model 3
        wls_model = sm.WLS(x_data, y_data,)
        results = wls_model.fit()
        print('model 3: ')
        print(results.summary())

    """