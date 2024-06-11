import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import data_handler as data
import regression as reg
import tools as tool
import graphs as graph

if __name__ == '__main__':
    df = data.prepare_data()

    m1 = reg.regression(df[df['prog_cons_score'] >= -250], 'sys_jus', ['fulfillment'])
    print(m1.summary())

    graph.scatter(df, 'fulfillment', 'sys_jus')
    graph.scatter(df, 'fulfillment', 'sys_jus', color_col='former_socialist_country', color_col_vals=[0, 1])
    graph.scatter(df[df['prog_cons_score'] >= -250], 'fulfillment', 'sys_jus', color_col='prog_con',
                  color_col_vals=['very progressive',
                                  'very conservative'])

    m2 = reg.regression(df, 'sys_jus', ['C(prog_con, Treatment(reference=\'moderate\'))',
                                        'C(female, Treatment(reference=0))'])
    print(m2.summary())

    m3 = reg.regression(df, 'sys_jus', ['prog_cons_score', 'C(female, Treatment(reference=0))',
                                        'satisfaction', 'sexism', 'C(social_class)'])
    print(m3.summary())

    m4 = reg.regression(df, 'sys_jus', ['fulfillment', 'sexism'])
    print(m4.summary())

    m5 = reg.regression(df, 'sys_jus', ['sexism'])
    print(m5.summary())

    m6 = reg.regression(df, 'sexism', ['fulfillment'])
    print(m6.summary())

    m7 = reg.regression(df, 'sys_jus', ['fulfillment', 'sexism', 'C(former_socialist_country)', 'age',
                                        'C(social_class)',
                                        'C(female)', 'satisfaction'])
    print(m7.summary())

    m8 = reg.regression(df, 'sys_jus', ['C(interview_conducted)'])
    print(m8.summary())

    # print(df['former_socialist_country'].describe())
    # plt.hist(df['former_socialist_country'])
    # plt.show()

    # graph.multiple_models_coefplot([m1], ['m1'])
