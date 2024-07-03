

# function to print rows with certain keywords
# input: dataframe and dict (e.g. {column1 : keyword1, column2 : keyword2}
def print_conditions(df, keyword_dict):
    count = 0
    for index, row in df.iterrows():
        flag_dict = dict()
        for key in keyword_dict:
            flag_dict[key] = False
        for key in keyword_dict:
            if row[key] == keyword_dict[key]:
                flag_dict[key] = True
        flag = True
        for f in flag_dict:
            if not flag_dict[f]:
                flag = False
        if flag:
            print(row)
            count = count + 1
    print('rows found: ' + str(count))


# saves description of certain variables to csv
def save_description(df, cols, filename):
    filename = filename + '.csv'
    df[cols].describe(include='all').round(4).to_csv(filename, sep=';')


