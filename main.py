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
    graph.scatter(df[df['prog_cons_score'] >= -250], 'fulfillment', 'sys_jus', color_col='prog_con',
                  color_col_vals=['very progressive',
                                  'very conservative'])

    m2 = reg.regression(df, 'sys_jus', ['C(prog_con, Treatment(reference=\'moderate\'))',
                                        'C(female, Treatment(reference=0))'])
    print(m2.summary())

    m3 = reg.regression(df, 'sys_jus', ['prog_cons_score', 'C(female, Treatment(reference=0))',
                                        'satisfaction', 'sexism', 'C(social_class)'])
    print(m3.summary())

    m4 = reg.regression(df, 'sys_jus', ['fulfillment', 'C(social_class)', 'sexism'])
    print(m4.summary())

    print(df['fulfillment_score_counter'].describe())
    plt.hist(df['fulfillment_score_counter'])
    plt.show()

    # graph.multiple_models_coefplot([m1], ['m1'])
