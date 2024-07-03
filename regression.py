import statsmodels.formula.api as smf


# general regression function
# input: DataFrame containing, variables, dependent & independent variables
# optional: intercept = False if intercept is not wanted
# returns OLS-regression model
def regression(df, dependent_var, independent_var_list, intercept=True):
    reg_str = dependent_var + ' ~ '
    i = 1
    var_len = len(independent_var_list)
    for var in independent_var_list:
        if i < var_len:
            reg_str = reg_str + var + ' + '
            i = i + 1
        else:
            reg_str = reg_str + var
    if not intercept:
        reg_str = reg_str + ' -1'
    try:
        model = smf.ols(formula=reg_str, data=df).fit()
    except:
        print('Error when running regression')
    return model
