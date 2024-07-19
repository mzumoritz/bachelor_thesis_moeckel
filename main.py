#!/usr/bin/env python

"""
\
Main file to run the code necessary for the bachelor thesis of Moritz Möckel Topic: Climate, Gender Roles & System
Justification: How does the fulfillment of gendered role expectations influence individuals’ engagement in system
justification?

The dataset must be located in the file path, as the files of this script
It can be downloaded here: https://search.gesis.org/research_data/ZA7503?doi=10.4232/1.14021

packages required:
pandas
matplotlib
stargazer
scipy
statsmodels
numpy
"""

import data_handler as data
import regression as reg
import tools as tool
import graphs as graph

__author__ = 'Moritz Möckel'
__email__ = 'mmoecke2@smail.uni-koeln.de'
__status__ = 'finished'
__date__ = '10.07.2024'

if __name__ == '__main__':
    # prepare dataset
    df = data.prepare_data()

    # create regression models
    m1 = reg.regression(df, 'sys_jus', ['fulfillment'])
    print(m1.summary())

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

    # save univariate description of variables to csv-file
    tool.save_description(df, ['sys_jus', 'fulfillment', 'sexism'], 'uni_main')
    tool.save_description(df, ['former_socialist_country', 'age', 'social_class',
                               'female'], 'uni_cov')

    # save regression outputs
    graph.create_html_table([m1, m2, m3, m4],
                            'main_output.html',
                            custom_columns=['m1', 'm2', 'm3', 'm4'],
                            show_model_numbers=False,
                            covariate_order=['Intercept', 'fulfillment', 'sexism'],
                            custom_notes=['Standard errors in parentheses.'],
                            dep_var_list=['sys_jus', 'sys_jus', 'sexism', 'sys_jus'])

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

    # create scatterplot with regression line
    graph.scatter_fit(df, 'fulfillment', 'sys_jus', r_sq=m1.rsquared, intercept=m1.params[0],
                      coef=m1.params[1])
