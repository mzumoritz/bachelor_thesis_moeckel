import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.iolib.summary2 import summary_col
from stargazer.stargazer import Stargazer, LineLocation
from IPython.core.display import HTML

import data_handler as data
import regression as reg
import tools as tool
import graphs as graph

if __name__ == '__main__':
    df = data.prepare_data()

    m1 = reg.regression(df, 'sys_jus', ['fulfillment'])
    print(m1.summary())

    # graph.scatter(df, 'fulfillment', 'sys_jus')
    # graph.scatter(df, 'fulfillment', 'sys_jus', color_col='former_socialist_country', color_col_vals=[0, 1])
    # graph.scatter(df[df['prog_cons_score'] >= -250], 'fulfillment', 'sys_jus', color_col='prog_con',
    #               color_col_vals=['very progressive',
    #                               'very conservative'])

    m2 = reg.regression(df, 'sys_jus', ['sexism'])
    print(m2.summary())

    m3 = reg.regression(df, 'sexism', ['fulfillment'])
    print(m3.summary())

    m4 = reg.regression(df, 'sys_jus', ['fulfillment', 'sexism'])
    print(m4.summary())

    m5 = reg.regression(df, 'sys_jus', ['fulfillment', 'sexism', 'former_socialist_country'])
    print(m5.summary())

    m6 = reg.regression(df, 'sys_jus', ['fulfillment', 'sexism', 'age'])
    print(m6.summary())

    m7 = reg.regression(df, 'sys_jus', ['fulfillment', 'sexism',
                                        'C(social_class, Treatment(reference=\'lower class\'))'])
    print(m7.summary())

    m8 = reg.regression(df, 'sys_jus', ['fulfillment', 'sexism',
                                        'C(female, Treatment(reference=0))'])
    print(m8.summary())

    m9 = reg.regression(df, 'sys_jus', ['fulfillment', 'sexism', 'former_socialist_country', 'age',
                                        'C(social_class, Treatment(reference=\'lower class\'))',
                                        'C(female, Treatment(reference=0))'])
    print(m9.summary())

    tool.save_description(df, ['sys_jus', 'fulfillment', 'sexism'], 'uni_main')
    tool.save_description(df, ['former_socialist_country', 'age', 'social_class',
                               'female'], 'uni_cov')

    main_output = summary_col([m1, m2, m3, m4], stars=True,
                              model_names=['m1\nsys_jus', 'm2\nsys_jus', 'm3\nsexism', 'm4\nsys_jus'])
    main_output.tables[0].to_csv("main_output.csv", sep=';', encoding='utf-8-sig')
    print(main_output)

    stargazer = Stargazer([m1, m2, m3, m4])
    graph.create_html_table([m1, m2, m3, m4],
                            'main_output.html',
                            custom_columns=['m1', 'm2', 'm3', 'm4'],
                            show_model_numbers=False,
                            covariate_order=['Intercept', 'fulfillment', 'sexism'],
                            custom_notes=['Standard errors in parentheses.'],
                            dep_var_list=['sys_jus', 'sys_jus', 'sexism', 'sys_jus'])

    cov_output = summary_col([m5, m6, m7, m8, m9], stars=True,
                             model_names=['m5\nsys_jus', 'm6\nsys_jus', 'm7\nsys_jus', 'm8\nsys_jus',
                                          'm9\nsys_jus'])
    cov_output.tables[0].to_csv("cov_output.csv", sep=';', encoding='utf-8-sig')
    print(cov_output)

    graph.create_html_table([m5, m6, m7, m8, m9],
                            'cov_output.html',
                            custom_columns=['m5', 'm6', 'm7', 'm8', 'm9'],
                            dep_var_list=['sys_jus', 'sys_jus', 'sys_jus', 'sys_jus', 'sys_jus'],
                            show_model_numbers=False,
                            covariate_order=['Intercept', 'fulfillment', 'sexism', 'former_socialist_country',
                                             'age',
                                             'C(social_class, Treatment(reference=\'lower class\'))[T.middle class]',
                                             'C(social_class, Treatment(reference=\'lower class\'))[T.upper class]',
                                             'C(female, Treatment(reference=0))[T.1]'],
                            custom_notes=['Standard errors in parentheses.'],
                            rename_covariates={'former_socialist_country': 'former socialist country',
                                               'C(social_class, Treatment(reference=\'lower class\'))[T.middle class]':
                                               'middle class',
                                               'C(social_class, Treatment(reference=\'lower class\'))[T.upper class]':
                                               'upper class',
                                               'C(female, Treatment(reference=0))[T.1]': 'female'})

    graph.scatter_fit(df, 'fulfillment', 'sys_jus', r_sq=m1.rsquared, intercept=m1.params[0],
                      coef=m1.params[1])

    # graph.multiple_models_coefplot([m1, m4], ['m1', 'm4'], remove_intercept=True)

    # print((df['education'] - df['edu_spouse']).describe())
    # plt.hist(df['education'] - df['edu_spouse'])
    # plt.show()

    print(df['social_class'].describe())
    # plt.hist(df['sys_jus'])
    # plt.show()

    x, y = np.unique(df['sys_jus'], return_counts=True)
    # plt.scatter(x, y)
    # plt.show()

    x, y = np.unique(df['fulfillment'], return_counts=True)
    # plt.scatter(x, y)
    # plt.show()

    x, y = np.unique(df['age'], return_counts=True)
    # plt.scatter(x, y)
    # plt.show()

    x, y = np.unique(df['female'], return_counts=True)
    print(x)
    print(y)

    # print(df['interview_conducted'].unique())
    # print(df.groupby('interview_conducted')['sys_jus'].mean())

    # graph.multiple_models_coefplot([m1], ['m1'])
