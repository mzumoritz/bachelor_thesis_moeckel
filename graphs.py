import matplotlib.pyplot as plt
import numpy as np
from stargazer.stargazer import Stargazer, LineLocation
import scipy.stats as stats


# plots a simple scatterplot
# different categories can be marked if the corresponding variable name and the categories to be marked are passed
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


# creates an HTML-table with regression result of the models passed
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


# creates a scatter plot featuring a fitted regression line
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
    ax.fill_between(xseq, y2 + pi, y2 - pi, color='None', linestyle='--')
    ax.plot(xseq, y2 - pi, '--', color='orange', label='95% Prediction Limits')
    ax.plot(xseq, y2 + pi, '--', color='orange')
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
        [label for i, label in enumerate(labels) if i in display] + ['95% Confidence Limits'],
        loc=9, bbox_to_anchor=(0, -0.21, 1., 0.102), ncol=3, mode='expand', fontsize=16
    )
    legend.get_frame().set_edgecolor('0.5')
    plt.grid()
    plt.tight_layout()
    plt.savefig('filename.png', bbox_extra_artists=(legend,), bbox_inches='tight')
    plt.show()


# necessary for scatter_fit
# plots confidence intervals
def plot_ci_manual(t, s_err, n, x, x2, y2, ax=None):
    if ax is None:
        ax = plt.gca()

    ci = t * s_err * np.sqrt(1 / n + (x2 - np.mean(x)) ** 2 / np.sum((x - np.mean(x)) ** 2))
    ax.fill_between(x2, y2 + ci, y2 - ci, color='mistyrose')

    return ax


# necessary for scatter_fit
# returns a numpy-equation
def equation(a, b):
    return np.polyval(a, b)
