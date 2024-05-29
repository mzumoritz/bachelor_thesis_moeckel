import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tools as tool
from matplotlib.lines import Line2D


def scatter(df, var_x, var_y, color_col='', color_col_vals=[]):
    df_list = list()
    color_list = ['blue', 'red', 'green', 'orange', 'yellow', 'purple', 'pink']
    if color_col != '':
        for val in color_col_vals:
            df_list.append(df[df[color_col] == val])
        i = 0
        for d in df_list:
            plt.scatter(d[var_x], d[var_y], c=color_list[i])
            plt.title(var_y + ' vs. ' + var_x)
            plt.ylabel(var_y)
            plt.xlabel(var_x)
            i = i + 1
        plt.grid()
        plt.show()
    else:
        plt.scatter(df[var_x], df[var_y])
        plt.title(var_y + ' vs. ' + var_x)
        plt.ylabel(var_y)
        plt.xlabel(var_x)
        plt.grid()
        plt.show()


def multiple_models_coefplot(models, modelnames, filename='multiple_coef.png', title=''):
    plt.style.use("ggplot")
    coef_df = pd.DataFrame()
    for i, mod in enumerate(models):
        err_series = mod.params - mod.conf_int()[0]
        coef_df = pd.concat([coef_df, pd.DataFrame({'coef': mod.params.values,
                                                    'err': err_series.values,
                                                    'varname': err_series.index.values,
                                                    'model': modelnames[i]
                                                    })], axis=0
                            )
    # print(coef_df.to_string())
    marker_pool = 'sodpP*H'
    marker_list = list()
    for i, m in enumerate(modelnames):
        marker_list.append(marker_pool[i])
    width = 1/len(models)
    base_y = np.arange(len(tool.delete_double(coef_df['varname'])))
    # print(base_y)
    base_y = base_y[::-1]
    # print(base_y)
    # base_y = np.arange(6) - 0.2
    y_labels = list()
    for val in tool.delete_double(coef_df['varname']):
        y_labels.append(val)
    y_labels.append('')
    y_labels.reverse()
    # print(y_labels)

    fig, ax = plt.subplots(figsize=(10, len(err_series) + len(err_series) / 2))
    # fig, ax = plt.subplots(figsize=(10, 25))
    mod_list = list(enumerate(coef_df.model.unique()))
    mod_list.reverse()
    # print(mod_list)
    for el in mod_list:
        i = el[0]
        mod = el[1]
        # print(i)
        # print(mod)
        mod_df = coef_df[coef_df.model == mod]
        mod_df = mod_df.set_index('varname').reindex(coef_df['varname'].unique())
        # print(mod_df)
        # offset y posistions
        Y = base_y - width * i
        # print(Y)
        ax.barh(Y, mod_df['coef'],
                color='none', xerr=mod_df['err'])
        # remove axis labels
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.scatter(x=mod_df['coef'],
                   marker=marker_list[i], s=120,
                   y=Y, color='black')
        ax.axvline(x=0, linestyle='-', color='red', linewidth=1)
        ax.yaxis.set_ticks_position('none')
        _ = ax.set_yticklabels(y_labels,
                               rotation=0, fontsize=16)
        # _ = ax.set_xticklabels(np.arange(-1, 1, 0.25),
        #                        rotation=0, fontsize=16)

    # finally, build customized legend
    legend_elements = [Line2D([0], [0], marker=m,
                              label=modelnames[i],
                              color='k',
                              markersize=10)
                       for i, m in enumerate(marker_list)
                       ]
    _ = ax.legend(handles=legend_elements, loc='lower right',
                  prop={'size': 15}, labelspacing=1.2)
    plt.grid(axis='x', color='black')
    plt.title(title, fontsize=16)
    plt.xticks(fontsize=16)
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.show()
    fig.clf()
    plt.close()
