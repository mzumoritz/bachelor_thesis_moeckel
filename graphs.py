import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tools as tool
from matplotlib.lines import Line2D
from stargazer.stargazer import Stargazer, LineLocation
import scipy.stats as stats


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


def multiple_models_coefplot(models, modelnames, filename='multiple_coef.png', title='', remove_intercept=False,
                             remove_coeffs=[]):
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
    if remove_intercept:
        coef_df = coef_df[coef_df.varname != 'Intercept']
    if len(remove_coeffs) > 0:
        for coeff in remove_coeffs:
            coef_df = coef_df[coef_df.varname != coeff]
    print(coef_df.to_string())
    marker_pool = 'sodpP*H'
    marker_list = list()
    for i, m in enumerate(modelnames):
        marker_list.append(marker_pool[i])
    width = 0.25
    base_y = np.arange(len(tool.delete_double(coef_df['varname'])))
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
        ## offset y posistions
        Y = base_y - width * i
        ax.barh(Y, mod_df['coef'],
                color='none', xerr=mod_df['err'])
        ## remove axis labels
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.scatter(x=mod_df['coef'],
                   marker=marker_list[i], s=120,
                   y=Y, color='black')
        ax.axvline(x=0, linestyle='--', color='black', linewidth=4)
        ax.yaxis.set_ticks_position('none')
        _ = ax.set_yticklabels(y_labels,
                               rotation=0, fontsize=16)
        # _ = ax.set_xticklabels(np.arange(-1, 1, 0.25),
        #                        rotation=0, fontsize=16)

    ## finally, build customized legend
    legend_elements = [Line2D([0], [0], marker=m,
                              label=modelnames[i],
                              color='k',
                              markersize=10)
                       for i, m in enumerate(marker_list)
                       ]
    _ = ax.legend(handles=legend_elements, loc=2,
                  prop={'size': 15}, labelspacing=1.2)
    plt.grid(axis='x', color='black')
    plt.title(title, fontsize=16)
    plt.xticks(fontsize=16)
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.show()
    fig.clf()
    plt.close()


def create_html_table(models,
                      filename,
                      title='',
                      custom_columns=[],
                      show_model_numbers=True,
                      significant_digits=4,
                      covariate_order=[],
                      rename_covariates={},
                      degrees_of_freedom=False,
                      custom_notes=[],
                      show_f_statistic=False,
                      show_n=False,
                      show_residual_std_error=False,
                      dep_var_list=[]):
    stargazer = Stargazer(models)
    if title != '':
        stargazer.title(title)
    if len(custom_columns) > 0:
        stargazer.custom_columns(custom_columns)
    stargazer.show_model_numbers(show_model_numbers)
    stargazer.significant_digits(significant_digits)
    if len(covariate_order) > 0:
        stargazer.covariate_order(covariate_order)
    if len(rename_covariates) > 0:
        stargazer.rename_covariates(rename_covariates)
    stargazer.show_degrees_of_freedom(degrees_of_freedom)
    stargazer.show_f_statistic = show_f_statistic
    stargazer.show_n = show_n
    stargazer.show_residual_std_err = show_residual_std_error
    if len(custom_notes) > 0:
        stargazer.add_custom_notes(custom_notes)
    if len(dep_var_list) > 0:
        stargazer.add_line('Dependent variable', dep_var_list, LineLocation.HEADER_BOTTOM)
    file = open(filename, 'w')
    file.write(stargazer.render_html())
    file.close()
    return stargazer


def scatter_fit(df, xtitle, ytitle, r_sq, intercept, coef, title=''):
    x = df[xtitle]
    y = df[ytitle]
    p, cov = np.polyfit(x, y, 1, cov=True)
    y_model = equation(p, x)
    n = y.size
    m = p.size
    dof = n - m
    t = stats.t.ppf(0.975, n - m)
    resid = y - y_model
    chi2 = np.sum((resid / y_model) ** 2)
    chi2_red = chi2 / dof
    s_err = np.sqrt(np.sum(resid ** 2) / dof)

    fig, ax = plt.subplots(figsize=(15, 9))
    ax.scatter(x, y, s=50, alpha=0.7, edgecolors='k')

    b, a = np.polyfit(x, y, deg=1)
    xseq = np.linspace(x.min(), x.max(), num=len(df))
    y2 = equation(p, xseq)

    ax.plot(xseq, a + b * xseq, color='r', lw=2.5, linestyle='--', label='Fit')
    ax.text(-1.4, 9, r'$R^2 =$' + str(round(r_sq, 4)), fontsize=16, weight='bold', horizontalalignment='left')
    ax.text(-1.4, 8.5, r'$\hat\beta_1 =$' + str(round(coef, 4)), fontsize=16, weight='bold',
            horizontalalignment='left')
    ax.text(-1.4, 8, r'$\hat\beta_0 =$' + str(round(intercept, 4)), fontsize=16, weight='bold',
            horizontalalignment='left')
    plot_ci_manual(t, s_err, n, x, xseq, y2, ax=ax)
    pi = t * s_err * np.sqrt(1 + 1 / n + (xseq - np.mean(x)) ** 2 / np.sum((x - np.mean(x)) ** 2))
    ax.fill_between(xseq, y2 + pi, y2 - pi, color="None", linestyle="--")
    ax.plot(xseq, y2 - pi, "--", color='orange', label='95% Prediction Limits')
    ax.plot(xseq, y2 + pi, "--", color='orange')
    # fig.tight_layout()
    ax.set_xlabel(xtitle, fontsize=16)
    ax.set_ylabel(ytitle, fontsize=16)
    # plt.rcParams.update({'font.size': 44})
    for label in (ax.get_xticklabels() + ax.get_yticklabels()): label.set_fontsize(12)
    handles, labels = ax.get_legend_handles_labels()
    display = (0, 1)
    anyArtist = plt.Line2D((0, 1), (0, 0), color='mistyrose', lw=5)
    legend = plt.legend(
        [handle for i, handle in enumerate(handles) if i in display] + [anyArtist],
        [label for i, label in enumerate(labels) if i in display] + ["95% Confidence Limits"],
        loc=9, bbox_to_anchor=(0, -0.21, 1., 0.102), ncol=3, mode="expand", fontsize=16
    )
    frame = legend.get_frame().set_edgecolor("0.5")
    plt.grid()
    plt.tight_layout()
    plt.savefig("filename.png", bbox_extra_artists=(legend,), bbox_inches="tight")
    plt.show()


# https://stackoverflow.com/questions/27164114/show-confidence-limits-and-prediction-limits-in-scatter-plot
def plot_ci_manual(t, s_err, n, x, x2, y2, ax=None):
    if ax is None:
        ax = plt.gca()

    ci = t * s_err * np.sqrt(1 / n + (x2 - np.mean(x)) ** 2 / np.sum((x - np.mean(x)) ** 2))
    ax.fill_between(x2, y2 + ci, y2 - ci, color='mistyrose')

    return ax


def equation(a, b):
    return np.polyval(a, b)
