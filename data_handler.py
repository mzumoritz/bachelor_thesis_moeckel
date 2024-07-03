import pandas as pd


# load data in dataframe and prepare it
# data file must be located in same directory as this file
# returns DataFrame
def prepare_data():
    df = pd.read_stata('evs_trend.dta', convert_categoricals=False)
    df = evs_2017(df)
    df = confounders(df)
    df = remove_non_democratic(df)
    df = sys_jus(df)
    df = prog_cons_score(df)
    df = fulfillment_score(df)
    df = fulfillment(df)
    df = sexism(df)
    return df


# preparation of potential confounding variables
# returns DataFrame including confounders
def confounders(df):
    df = social_class(df)
    df = former_socialist_country(df)
    df = age(df)
    df = female(df)
    return df


# remove non-democratic countries
# returns DataFrame with participants from non-democratic countries removed
def remove_non_democratic(df):
    df = df[df.interview_conducted != 'AL']
    df = df[df.interview_conducted != 'AM']
    df = df[df.S003 != 31]
    df = df[df.interview_conducted != 'BY']
    df = df[df.interview_conducted != 'BA']
    df = df[df.interview_conducted != 'GE']
    df = df[df.interview_conducted != 'ME']
    df = df[df.interview_conducted != 'MK']
    df = df[df.interview_conducted != 'RU']
    df = df[df.interview_conducted != 'UA']
    df = df[df.interview_conducted != 'TR']
    df = df[df.interview_conducted != 'CY-TCC']
    df = df[df.interview_conducted != 'RS-KM']
    df = df[df.interview_conducted != 'MD']
    return df


# does participant live in former socialist country
# returns DataFrame with dummy-coded variable
# 0 = not from former socialist country
# 1 = from former socialist country
def former_socialist_country(df):
    socialist_country_list = ['AL', 'AM', 'BA', 'BG', 'BY', 'CZ', 'EE', 'GE', 'HR', 'HU', 'RS-KM', 'LT', 'LV', 'MD',
                              'ME', 'MK', 'PL', 'RS', 'RO', 'RU', 'SI', 'SK', 'UA']
    df['interview_conducted'] = df['S009']
    # remove missing
    df = df[df.interview_conducted != -5]
    df = df[df.interview_conducted != -4]
    df = df[df.interview_conducted != -3]
    df = df[df.interview_conducted != -2]
    df = df[df.interview_conducted != -1]
    df = df[df.X002_02A != -5]
    df = df[df.X002_02A != -4]
    df = df[df.X002_02A != -3]
    df = df[df.X002_02A != -2]
    df = df[df.X002_02A != -1]
    val_list = list()
    for index, row in df.iterrows():
        if row['interview_conducted'] in socialist_country_list:
            val_list.append(1)
        # for germany check if east germany (were born)
        elif row['interview_conducted'] == 'DE':
            if row['X002_02A'] == 278:
                val_list.append(1)
            else:
                val_list.append(0)
        else:
            val_list.append(0)
    df['former_socialist_country'] = val_list
    return df


# returns DataFrame which only contains the EVS 2017
def evs_2017(df):
    # only evs 2017
    df = df[df.s002vs == 7]
    return df


# position on economy vs. environment for sys_jus
# returns DataFrame including variable econ_env
def econ_env(df):
    # create variable economy vs environment econ_env
    df['econ_env'] = df['B008']
    # remove missing for environment vs. economy & other
    df = df[df.econ_env != -5]
    df = df[df.econ_env != -4]
    df = df[df.econ_env != -3]
    df = df[df.econ_env != -2]
    df = df[df.econ_env != -1]
    df = df[df.econ_env != 3]
    # recode econ_env
    # Environment = 0
    # Economy = 9
    df['econ_env'] = df['econ_env'].replace([1], 0)
    df['econ_env'] = df['econ_env'].replace([2], 9)
    return df


# position on income inequality for sys_jus
# returns Dataframe including variable inc_eneq
def inc_ineq(df):
    df['inc_ineq'] = df['E035']
    # remove missing
    df = df[df.inc_ineq != -5]
    df = df[df.inc_ineq != -4]
    df = df[df.inc_ineq != -3]
    df = df[df.inc_ineq != -2]
    df = df[df.inc_ineq != -1]
    # recode
    # all values -1
    df['inc_ineq'] = df['inc_ineq'].replace([1], 0)
    df['inc_ineq'] = df['inc_ineq'].replace([2], 1)
    df['inc_ineq'] = df['inc_ineq'].replace([3], 2)
    df['inc_ineq'] = df['inc_ineq'].replace([4], 3)
    df['inc_ineq'] = df['inc_ineq'].replace([5], 4)
    df['inc_ineq'] = df['inc_ineq'].replace([6], 5)
    df['inc_ineq'] = df['inc_ineq'].replace([7], 6)
    df['inc_ineq'] = df['inc_ineq'].replace([8], 7)
    df['inc_ineq'] = df['inc_ineq'].replace([9], 8)
    df['inc_ineq'] = df['inc_ineq'].replace([10], 9)
    return df


# position on how important it is to have [respondent's] ancestry for sys_jus
# returns DataFrame including variable imp_ancestry
def imp_ancestry(df):
    df['imp_ancestry'] = df['G035']
    # remove missing
    df = df[df.imp_ancestry != -5]
    df = df[df.imp_ancestry != -4]
    df = df[df.imp_ancestry != -3]
    df = df[df.imp_ancestry != -2]
    df = df[df.imp_ancestry != -1]
    # 0 = not important at all
    # 3 = not important
    # 6 = quite important
    # 9 = very important
    df['imp_ancestry'] = df['imp_ancestry'].replace([4], 0)
    df['imp_ancestry'] = df['imp_ancestry'].replace([2], 6)
    df['imp_ancestry'] = df['imp_ancestry'].replace([1], 9)
    return df


# position on how important it is to respect [respondent's] country's political institutions and laws for sys_jus
# returns DataFrame including variable respect_inst_laws
def respect_inst_laws(df):
    df['respect_inst_laws'] = df['G034']
    # remove missing
    df = df[df.respect_inst_laws != -5]
    df = df[df.respect_inst_laws != -4]
    df = df[df.respect_inst_laws != -3]
    df = df[df.respect_inst_laws != -2]
    df = df[df.respect_inst_laws != -1]
    # 0 = not important at all
    # 3 = not important
    # 6 = quite important
    # 9 = very important
    df['respect_inst_laws'] = df['respect_inst_laws'].replace([4], 0)
    df['respect_inst_laws'] = df['respect_inst_laws'].replace([2], 6)
    df['respect_inst_laws'] = df['respect_inst_laws'].replace([1], 9)
    return df


# position on statement 'work is a duty towards society' for sys_jus
# returns DataFrame including variable duty_work
def duty_work(df):
    df['duty_work'] = df['C039']
    # remove missing
    df = df[df.duty_work != -5]
    df = df[df.duty_work != -4]
    df = df[df.duty_work != -3]
    df = df[df.duty_work != -2]
    df = df[df.duty_work != -1]
    # recode
    # 0 = strongly disagree
    # 2.25 = disagree
    # 4.5 = neither agree nor disagree
    # 6.75 = agree
    # 9 = strongly agree
    df['duty_work'] = df['duty_work'].replace([5], 0)
    df['duty_work'] = df['duty_work'].replace([4], 2.25)
    df['duty_work'] = df['duty_work'].replace([3], 4.5)
    df['duty_work'] = df['duty_work'].replace([2], 6.75)
    df['duty_work'] = df['duty_work'].replace([1], 9)
    return df


# social class variable (possible confounder)
# returns DataFrame including variable social class
def social_class(df):
    df['social_class'] = df['X036C']
    # remove missing
    df = df[df.social_class != -5]
    df = df[df.social_class != -4]
    df = df[df.social_class != -2]
    df = df[df.social_class != -1]
    # recode
    # upper class: higher controllers (1), self-employed with employees (5), self-employed farmer (11)
    # middle class: lower controllers (2), routine non manual (3), lower sales-service (4),
    #   self employed with no employees (6), manual supervisors (7), skilled worker (8)
    # lower class: unemployed (-3), unskilled worker (9), farm labor (10)
    df['social_class'] = df['social_class'].replace([1, 5, 11], 'upper class')
    df['social_class'] = df['social_class'].replace([2, 3, 4, 6, 7, 8], 'middle class')
    df['social_class'] = df['social_class'].replace([-3, 9, 10], 'lower class')
    return df


# positioning on left right scale for sys_jus
# 0 = left
# 9 = right
# returns DataFrame including variable left_right
def left_right(df):
    df['left_right'] = df['E033']
    # remove missing
    df = df[df.left_right != -5]
    df = df[df.left_right != -4]
    df = df[df.left_right != -3]
    df = df[df.left_right != -2]
    df = df[df.left_right != -1]
    # recode
    i = 1
    while i <= 10:
        df['left_right'] = df['left_right'].replace([i], i - 1)
        i = i + 1
    return df


# position on statement 'people who don't work turn lazy' for sys_jus
# returns DataFrame including variable no_work_lazy
def no_work_lazy(df):
    df['no_work_lazy'] = df['C038']
    # remove missing
    df = df[df.no_work_lazy != -5]
    df = df[df.no_work_lazy != -4]
    df = df[df.no_work_lazy != -3]
    df = df[df.no_work_lazy != -2]
    df = df[df.no_work_lazy != -1]
    # recode
    # 0 = strongly disagree
    # 2.25 = disagree
    # 4.5 = neither agree nor disagree
    # 6.75 = agree
    # 9 = strongly agree
    df['no_work_lazy'] = df['no_work_lazy'].replace([5], 0)
    df['no_work_lazy'] = df['no_work_lazy'].replace([4], 2.25)
    df['no_work_lazy'] = df['no_work_lazy'].replace([3], 4.5)
    df['no_work_lazy'] = df['no_work_lazy'].replace([2], 6.75)
    df['no_work_lazy'] = df['no_work_lazy'].replace([1], 9)
    return df


# position on statement 'when jobs are scarce, men have more right to a job than women'
# returns DataFrame including variable men_right_job
def men_right_job(df):
    df['men_right_job'] = df['C001_01']
    # remove missing
    df = df[df.men_right_job != -5]
    df = df[df.men_right_job != -4]
    df = df[df.men_right_job != -3]
    df = df[df.men_right_job != -2]
    df = df[df.men_right_job != -1]
    # recode
    # 0 = strongly disagree
    # 2.25 = disagree
    # 4.5 = neither agree nor disagree
    # 6.75 = agree
    # 9 = strongly agree
    df['men_right_job'] = df['men_right_job'].replace([5], 0)
    df['men_right_job'] = df['men_right_job'].replace([4], 2.25)
    df['men_right_job'] = df['men_right_job'].replace([3], 4.5)
    df['men_right_job'] = df['men_right_job'].replace([2], 6.75)
    df['men_right_job'] = df['men_right_job'].replace([1], 9)
    return df


# system justification variable
# calls all functions to create necessary variables
# returns DataFrame including variable sys_jus
def sys_jus(df):
    df = econ_env(df)
    df = inc_ineq(df)
    df = imp_ancestry(df)
    df = respect_inst_laws(df)
    df = no_work_lazy(df)
    df = left_right(df)
    df = duty_work(df)
    df = men_right_job(df)
    df['sys_jus'] = (df['econ_env'] +
                     df['inc_ineq'] +
                     df['imp_ancestry'] +
                     df['respect_inst_laws'] +
                     df['no_work_lazy'] +
                     df['left_right'] +
                     df['duty_work'] +
                     df['men_right_job']) / 8
    return df


# assign progressive/conservative category
# very progressive (score <= -75)
# progressive ( -50 <= score < -75)
# slightly progressive (-25 <= score < -50)
# moderate (-25 < score < 25)
# slightly conservative (25 <= score < 50)
# conservative (50 <= score < 75)
# very conservative (score >= 75)
# returns DataFrame including variable prog_con
def assign_prog_con(df):
    pc_list = list()
    for index, row in df.iterrows():
        if row['prog_cons_score'] <= -0.75:
            pc_list.append('very progressive')
        elif -0.50 >= row['prog_cons_score'] > -0.75:
            pc_list.append('progressive')
        elif -0.25 >= row['prog_cons_score'] > -0.50:
            pc_list.append('slightly progressive')
        elif -0.25 < row['prog_cons_score'] < 0.25:
            pc_list.append('moderate')
        elif 0.25 <= row['prog_cons_score'] < 0.50:
            pc_list.append('slightly conservative')
        elif 0.50 <= row['prog_cons_score'] < 0.75:
            pc_list.append('conservative')
        elif row['prog_cons_score'] >= 0.75:
            pc_list.append('very conservative')
        else:
            print(row['prog_cons_score'])
            pc_list.append('elel')
    df['prog_con'] = pc_list
    return df


# variable depicting age of respondent
# keep only if 18 or older
# returns DataFrame including variable age
def age(df):
    df['age'] = df['X003']
    # remove missing
    df = df[df.age != -5]
    df = df[df.age != -4]
    df = df[df.age != -3]
    df = df[df.age != -2]
    df = df[df.age != -1]
    # remove age < 18
    df = df[df.age >= 18]
    return df


# position on statement 'women want home and child' for prog_cons_score
# returns DataFrame including variable wom_hom_child
def wom_hom_child(df):
    df['wom_hom_child'] = df['D062']
    # remove missing
    df = df[df.wom_hom_child != -5]
    df = df[df.wom_hom_child != -4]
    df = df[df.wom_hom_child != -3]
    df = df[df.wom_hom_child != -2]
    df = df[df.wom_hom_child != -1]
    # recode
    # -1 = strongly disagree
    # -0.5 = disagree
    # 0.5 = agree
    # 1 = strongly agree
    df['wom_hom_child'] = df['wom_hom_child'].replace([4], -1)
    df['wom_hom_child'] = df['wom_hom_child'].replace([2], 0.5)
    df['wom_hom_child'] = df['wom_hom_child'].replace([3], -0.5)
    return df


# variable depicting respondents gender
# dummy-coded with female = 1
# returns DataFrame including variable female
def female(df):
    df['female'] = df['X001']
    # remove missing
    df = df[df.female != -5]
    df = df[df.female != -4]
    df = df[df.female != -3]
    df = df[df.female != -2]
    df = df[df.female != -1]
    # recode
    # 0 = male
    # 1 = female
    df['female'] = df['female'].replace([1], 0)
    df['female'] = df['female'].replace([2], 1)
    return df


# position on statement 'pre-school child suffers from working mother' for prog_cons_score
# returns DataFrame including variable child_suffers
def child_suffers(df):
    df['child_suffers'] = df['D061']
    # remove missing
    df = df[df.child_suffers != -5]
    df = df[df.child_suffers != -4]
    df = df[df.child_suffers != -3]
    df = df[df.child_suffers != -2]
    df = df[df.child_suffers != -1]
    # recode
    # -1 = strongly disagree
    # -0.5 = disagree
    # 0.5 = agree
    # 1 = strongly agree
    df['child_suffers'] = df['child_suffers'].replace([4], -1)
    df['child_suffers'] = df['child_suffers'].replace([3], -0.5)
    df['child_suffers'] = df['child_suffers'].replace([2], 0.5)
    return df


# position on statement 'it is a duty towards society to have children' for prog_cons_score
# returns DataFrame including variable duty_children
def duty_children(df):
    df['duty_children'] = df['D026_03']
    # remove missing
    df = df[df.duty_children != -5]
    df = df[df.duty_children != -4]
    df = df[df.duty_children != -3]
    df = df[df.duty_children != -2]
    df = df[df.duty_children != -1]
    # recode
    # -1 = strongly disagree
    # -0.5 = disagree
    # 0 = agree nor disagree
    # 0.5 = agree
    # 1 = strongly agree
    df['duty_children'] = df['duty_children'].replace([5], -1)
    df['duty_children'] = df['duty_children'].replace([4], -0.5)
    df['duty_children'] = df['duty_children'].replace([3], 0)
    df['duty_children'] = df['duty_children'].replace([2], 0.5)
    return df


# position on statement 'marriage is an outdated institution' for prog_cons_score
# returns DataFrame including variable marry_outdated
def marry_outdated(df):
    df['marry_outdated'] = df['D022']
    # remove missing
    # keep don't know (-1)
    df = df[df.marry_outdated != -5]
    df = df[df.marry_outdated != -4]
    df = df[df.marry_outdated != -3]
    df = df[df.marry_outdated != -2]
    # recode
    # agree = -1
    # don't know = 0
    # disagree = 1
    df['marry_outdated'] = df['marry_outdated'].replace([1], 10)
    df['marry_outdated'] = df['marry_outdated'].replace([0], 1)
    df['marry_outdated'] = df['marry_outdated'].replace([-1], 0)
    df['marry_outdated'] = df['marry_outdated'].replace([10], -1)
    return df


# importance of children for marriage for prog_cons_score
# returns DataFrame including variable imp_marry_child
def imp_marry_child(df):
    df['imp_marry_child'] = df['D038']
    # remove missing
    df = df[df.imp_marry_child != -5]
    df = df[df.imp_marry_child != -4]
    df = df[df.imp_marry_child != -3]
    df = df[df.imp_marry_child != -2]
    df = df[df.imp_marry_child != -1]
    # recode
    # not very important = -1
    # rather important = 0
    # very important = 1
    df['imp_marry_child'] = df['imp_marry_child'].replace([2], 0)
    df['imp_marry_child'] = df['imp_marry_child'].replace([3], -1)
    return df


# how important is work in life for prog_cons_score
# returns DataFrame including variable imp_work
def imp_work(df):
    df['imp_work'] = df['A005']
    # remove missing
    df = df[df.imp_work != -5]
    df = df[df.imp_work != -4]
    df = df[df.imp_work != -3]
    df = df[df.imp_work != -2]
    df = df[df.imp_work != -1]
    # recode
    # not at all important = -1
    # not very important = -0.5
    # rather important = 0.5
    # very important = 1
    df['imp_work'] = df['imp_work'].replace([4], -1)
    df['imp_work'] = df['imp_work'].replace([3], -0.5)
    df['imp_work'] = df['imp_work'].replace([2], 0.5)
    return df


# decrease of importance placed on work in life for prog_cons_score
# returns DataFrame including variable dec_work
def dec_work(df):
    df['dec_work'] = df['E015']
    # remove missing
    df = df[df.dec_work != -5]
    df = df[df.dec_work != -4]
    df = df[df.dec_work != -3]
    df = df[df.dec_work != -2]
    df = df[df.dec_work != -1]
    # recode
    # good thing = -1
    # don't mind = 0
    # bad thing = 1
    df['dec_work'] = df['dec_work'].replace([1], -1)
    df['dec_work'] = df['dec_work'].replace([2], 0)
    df['dec_work'] = df['dec_work'].replace([3], 1)
    return df


# university is more important for a boy than for a girl for prog_cons_score
# -1 = strongly disagree
# -0.5 = disagree
# 0.5 = agree
# 1 = strongly agree
# returns DataFrame including variable university_important_prog_cons
def university_important_prog_cons(df):
    # remove missing
    df['university_important_prog_cons'] = df['D060']
    df = df[df.university_important_prog_cons != -5]
    df = df[df.university_important_prog_cons != -4]
    df = df[df.university_important_prog_cons != -3]
    df = df[df.university_important_prog_cons != -2]
    df = df[df.university_important_prog_cons != -1]
    # recode
    # -1 = strongly disagree
    # -0.5 = disagree
    # 0.5 = agree
    # 1 = strongly agree
    df['university_important_prog_cons'] = df['university_important_prog_cons'].replace([4], 0)
    df['university_important_prog_cons'] = df['university_important_prog_cons'].replace([2], 0.5)
    df['university_important_prog_cons'] = df['university_important_prog_cons'].replace([3], -0.5)
    return df


# progressive vs. conservative score
# negative is progressive, positive is conservative
# values between -1 and 1
# returns DataFrame including variable prog_cons_score
def prog_cons_score(df):
    df = marry_outdated(df)
    df = duty_children(df)
    df = imp_marry_child(df)
    df = child_suffers(df)
    df = wom_hom_child(df)
    df = imp_work(df)
    df = university_important_prog_cons(df)
    score_list = list()
    for index, row in df.iterrows():
        score = 0
        score = score + row['marry_outdated']
        score = score + row['duty_children']
        score = score + row['imp_marry_child']
        score = score + row['child_suffers']
        score = score + row['wom_hom_child']
        score = score + row['university_important_prog_cons']
        if row['female'] == 1:
            score = score - row['imp_work']
            # score = score - row['dec_work']
        else:
            score = score + row['imp_work']
            # score = score + row['dec_work']
        score = score / 7
        # print(str(score))
        score_list.append(score)
    df['prog_cons_score'] = score_list
    df = assign_prog_con(df)
    return df


# how many children for fulfillment_score
# returns DataFrame including variable children
def children(df):
    df['children'] = df['X011']
    # remove missing
    df = df[df.children != -5]
    df = df[df.children != -4]
    df = df[df.children != -3]
    df = df[df.children != -2]
    df = df[df.children != -1]
    return df


# employment status for fulfillment_score
# 1 = full time
# 2 = part-time
# 3 = Unemployed
# 4 = housewife
# 5 = others
# returns DataFrame including variable work
def work(df):
    df['work'] = df['X028']
    # remove missing
    df = df[df.work != -5]
    df = df[df.work != -4]
    df = df[df.work != -3]
    df = df[df.work != -2]
    df = df[df.work != -1]
    # remove retired, student & other
    # df = df[df.work != 4]
    # df = df[df.work != 6]
    # df = df[df.work != 8]
    # recode
    # 1 = full time & self-employed
    # 2 = part-time
    # 3 = Unemployed
    # 4 = housewife
    # 5 = others (retired, student, etc.)
    df['work'] = df['work'].replace([3], 1)
    df['work'] = df['work'].replace([7], 3)
    df['work'] = df['work'].replace([5], 10)
    df['work'] = df['work'].replace([4, 6, 8], 5)
    df['work'] = df['work'].replace([10], 4)
    return df


# employment status of partner for fulfillment_score
# 1 = full time
# 2 = part-time
# 3 = Unemployed
# 4 = housewife
# 5 = others
# returns DataFrame including variable work_partner
def work_partner(df):
    df['work_partner'] = df['W003']
    # remove missing
    df = df[df.work_partner != -5]
    df = df[df.work_partner != -4]
    df = df[df.work_partner != -3]
    df = df[df.work_partner != -2]
    df = df[df.work_partner != -1]
    # remove retired, student, disabled & other
    # df = df[df.work_partner != 5]
    # df = df[df.work_partner != 7]
    # df = df[df.work_partner != 9]
    # df = df[df.work_partner != 10]
    # recode
    # self-employed = 1
    # military service = 1
    # unemployed = 3
    # housewife = 4
    df['work_partner'] = df['work_partner'].replace([3, 4], 1)
    df['work_partner'] = df['work_partner'].replace([8], 3)
    df['work_partner'] = df['work_partner'].replace([6], 4)
    df['work_partner'] = df['work_partner'].replace([7, 9, 10], 5)
    return df


# marital status for fulfillment_score
# 1 = married
# 2 = previously married
# 3 = never married
# returns DataFrame including variable married
def married(df):
    df['married'] = df['X007']
    # remove missing
    df = df[df.married != -5]
    df = df[df.married != -4]
    df = df[df.married != -3]
    df = df[df.married != -2]
    df = df[df.married != -1]
    # recode
    # living together as married = 1
    # divorced = 2
    # separated = 2
    # widowed = 2
    # single/never married = 3
    df['married'] = df['married'].replace([2], 1)
    df['married'] = df['married'].replace([3, 4, 5], 2)
    df['married'] = df['married'].replace([6], 3)
    return df


# living together with partner for fulfillment_score
# -3 = not applicable (married)
# 0 = no
# 1 = yes
# returns DataFrame including variable living_with_partner
def living_with_partner(df):
    df['living_with_partner'] = df['X007_02']
    # remove missing
    df = df[df.living_with_partner != -5]
    df = df[df.living_with_partner != -4]
    # df = df[df.living_with_partner != -3]
    df = df[df.living_with_partner != -2]
    df = df[df.living_with_partner != -1]
    return df


# living in a stable relationship for fulfillment_score
# -3 = not applicable (married or living together)
# 0 = no
# 1 = yes
# returns DataFrame including variable stable_relationship
def stable_relationship(df):
    df['stable_relationship'] = df['X004']
    # remove missing
    df = df[df.stable_relationship != -5]
    df = df[df.stable_relationship != -4]
    # df = df[df.stable_relationship != -3]
    df = df[df.stable_relationship != -2]
    df = df[df.stable_relationship != -1]
    return df


# educational level of respondent for fulfillment_score
# 1 Inadequately completed elementary education
# 2 Completed (compulsory) elementary education
# 3 Incomplete secondary school: technical/vocational type
# 4 Complete secondary school: technical/vocational type/secondary
# 5 Incomplete secondary: university-preparatory type/secondary,
# 6 Complete secondary: university-preparatory type/full secondary
# 7 Some university without degree/higher education - lower-level tertiary
# 8 University with degree/higher education - upper-level tertiary
# returns DataFrame including variable education
def education(df):
    df['education'] = df['X025']
    # remove missing
    df = df[df.education != -5]
    df = df[df.education != -4]
    df = df[df.education != -3]
    df = df[df.education != -2]
    df = df[df.education != -1]
    return df


# educational level of spouse for fulfillment_score
# 1 Inadequately completed elementary education
# 2 Completed (compulsory) elementary education
# 3 Incomplete secondary school: technical/vocational type
# 4 Complete secondary school: technical/vocational type/secondary
# 5 Incomplete secondary: university-preparatory type/secondary,
# 6 Complete secondary: university-preparatory type/full secondary
# 7 Some university without degree/higher education - lower-level tertiary
# 8 University with degree/higher education - upper-level tertiary
# returns DataFrame including variable edu_spouse
def edu_spouse(df):
    df['edu_spouse'] = df['W002E']
    # remove missing
    df = df[df.edu_spouse != -5]
    df = df[df.edu_spouse != -4]
    # df = df[df.stable_relationship != -3]
    df = df[df.edu_spouse != -2]
    df = df[df.edu_spouse != -1]
    return df


# score about fulfillment of gender-roles
# -1 = fulfilling most progressive role
# 1 = fulfilling most conservative role
# returns DataFrame including variable fulfillment_score
def fulfillment_score(df):
    df = children(df)
    df = married(df)
    df = living_with_partner(df)
    df = stable_relationship(df)
    df = work(df)
    df = work_partner(df)
    df = dec_work(df)
    df = education(df)
    df = edu_spouse(df)
    score_list = list()
    score_counter_list = list()
    for index, row in df.iterrows():
        score = 0
        score_counter = 0

        # no. of children
        # if number of children <= 5: score = -1 + 2*(number of children / 5)
        # else score = 1
        if row['children'] <= 5:
            score = score + (- 1 + 2 * (row['children'] / 5))
            score_counter = score_counter + 1
        else:
            score = score + 1
            score_counter = score_counter + 1

        # if children: under which conditions
        # 1 if married
        # 0.5 if living with partner
        # -0.5 if in stable relationship
        # - 1 if not in stable relationship
        if row['children'] > 0:
            if row['married'] == 1:
                score = score + 1
                score_counter = score_counter + 1
            elif row['living_with_partner'] == 1:
                score = score + 0.5
                score_counter = score_counter + 1
            elif row['stable_relationship'] == 1:
                score = score - 0.5
                score_counter = score_counter + 1
            else:
                score = score - 1
                score_counter = score_counter + 1

        # child suffers if mother works
        # if children
        # if female more conservative if less work
        # if male more conservative if partner less work
        if row['children'] > 0:
            if row['female'] == 1:
                if row['work'] == 1:
                    score = score - 1
                    score_counter = score_counter + 1
                elif row['work'] == 2:
                    score = score - 0.5
                    score_counter = score_counter + 1
                elif row['work'] == 3:
                    score = score + 0.5
                    score_counter = score_counter + 1
                elif row['work'] == 4:
                    score = score + 1
                    score_counter = score_counter + 1
                else:
                    score_counter = score_counter + 1
            else:
                if row['work_partner'] == 1:
                    score = score - 1
                    score_counter = score_counter + 1
                elif row['work_partner'] == 2:
                    score = score - 0.5
                    score_counter = score_counter + 1
                elif row['work_partner'] == 3:
                    score = score + 0.5
                    score_counter = score_counter + 1
                elif row['work_partner'] == 4:
                    score = score + 1
                    score_counter = score_counter + 1
                else:
                    score_counter = score_counter + 1

        # married
        # yes = 1
        # previously = 0
        # never = -1
        if row['married'] == 1:
            score = score + 1
            score_counter = score_counter + 1
        elif row['married'] == 2:
            score_counter = score_counter + 1
        elif row['married'] == 3:
            score = score - 1
            score_counter = score_counter + 1

        # children important for marriage
        # if number of children <= 5: score = -1 + 2*(number of children / 5)
        # else score = 1
        if row['married'] < 3:
            if row['children'] <= 5:
                score = score + (- 1 + 2 * (row['children'] / 5))
                score_counter = score_counter + 1
            else:
                score = score + 1
                score_counter = score_counter + 1

        # work
        # if female: more work = more progressive
        # if male: more work = more conservative
        if row['female'] == 1:
            if row['work'] == 1:
                score = score - 1
                score_counter = score_counter + 1
            elif row['work'] == 2:
                score = score - 0.5
                score_counter = score_counter + 1
            elif row['work'] == 3:
                score = score + 0.5
                score_counter = score_counter + 1
            elif row['work'] == 4:
                score = score + 1
                score_counter = score_counter + 1
            else:
                score_counter = score_counter + 1
        else:
            if row['work'] == 1:
                score = score + 1
                score_counter = score_counter + 1
            elif row['work'] == 2:
                score = score + 0.5
                score_counter = score_counter + 1
            elif row['work'] == 3:
                score = score - 0.5
                score_counter = score_counter + 1
            elif row['work'] == 4:
                score = score - 1
                score_counter = score_counter + 1
            else:
                score_counter = score_counter + 1

        # could imagine working less
        # conservative for women
        # progressive for men
        if row['work'] < 3:
            if row['female'] == 1:
                score = score + (-1 * row['dec_work'])
                score_counter = score_counter + 1
            else:
                score = score + row['dec_work']
                score_counter = score_counter + 1

        # if in relationship: difference in education level
        # women more progressive, if higher education than spouse
        # men more conservative, if higher education than spouse
        if row['stable_relationship'] == 1 or row['stable_relationship'] == -3:
            education_difference = row['education'] - row['edu_spouse']
            if row['female'] == 1:
                score = score + (education_difference / 7)
                score_counter = score_counter + 1
            else:
                score = score - (education_difference / 7)
                score_counter = score_counter + 1

        # education level:
        # higher more progressive for women
        # lower more progressive for men
        if row['female'] == 1:
            score = score + (1 - 2 * (-1 + row['education']) / 7)
            score_counter = score_counter + 1
        else:
            score = score + (-1 + 2 * (-1 + row['education']) / 7)
            score_counter = score_counter + 1

        score = score / score_counter
        score_list.append(score)
        score_counter_list.append(score_counter)
    df['fulfillment_score'] = score_list
    df['fulfillment_score_counter'] = score_counter_list
    return df


# measure of fulfillment of self-perceived gender-role
# difference of prog_cons_score and fulfillment_score
# 0 = perfect fulfillment of self-perceived role
def fulfillment(df):
    df['fulfillment'] = (df['prog_cons_score'] - df['fulfillment_score'])
    return df


# absolute value of fulfillment
def fulfillment_abs(df):
    df['fulfillment_abs'] = abs(df['fulfillment'])
    return df


# z-standardization of fulfillment
def fulfillment_z(df):
    df['fulfillment_z'] = (df['fulfillment'] - df['fulfillment'].mean()) / df['fulfillment'].std()
    return df


# absolute value of z-standardization of fulfillment
def fulfillment_z_abs(df):
    df['fulfillment_z_abs'] = abs(df['fulfillment_z'])
    return df


# men make better political leaders than women do
# 0 = strongly disagree
# 3 = disagree
# 6 = agree
# 9 = strongly agree
def men_better_leaders(df):
    # remove missing
    df['men_better_leaders'] = df['D059']
    df = df[df.men_better_leaders != -5]
    df = df[df.men_better_leaders != -4]
    df = df[df.men_better_leaders != -3]
    df = df[df.men_better_leaders != -2]
    df = df[df.men_better_leaders != -1]
    # recode
    # 0 = strongly disagree
    # 3 = disagree
    # 6 = agree
    # 9 = strongly agree
    df['men_better_leaders'] = df['men_better_leaders'].replace([4], 0)
    df['men_better_leaders'] = df['men_better_leaders'].replace([2], 6)
    df['men_better_leaders'] = df['men_better_leaders'].replace([1], 9)
    return df


# men make better business executives than women do
# 0 = strongly disagree
# 3 = disagree
# 6 = agree
# 9 = strongly agree
def men_better_executives(df):
    # remove missing
    df['men_better_executives'] = df['D078']
    df = df[df.men_better_executives != -5]
    df = df[df.men_better_executives != -4]
    df = df[df.men_better_executives != -3]
    df = df[df.men_better_executives != -2]
    df = df[df.men_better_executives != -1]
    # recode
    # 0 = strongly disagree
    # 3 = disagree
    # 6 = agree
    # 9 = strongly agree
    df['men_better_executives'] = df['men_better_executives'].replace([4], 0)
    df['men_better_executives'] = df['men_better_executives'].replace([2], 6)
    df['men_better_executives'] = df['men_better_executives'].replace([1], 9)
    return df


# university is more important for a boy than for a girl
# 0 = strongly disagree
# 3 = disagree
# 6 = agree
# 9 = strongly agree
def university_important(df):
    # remove missing
    df['university_important'] = df['D060']
    df = df[df.university_important != -5]
    df = df[df.university_important != -4]
    df = df[df.university_important != -3]
    df = df[df.university_important != -2]
    df = df[df.university_important != -1]
    # recode
    # 0 = strongly disagree
    # 3 = disagree
    # 6 = agree
    # 9 = strongly agree
    df['university_important'] = df['university_important'].replace([4], 0)
    df['university_important'] = df['university_important'].replace([2], 6)
    df['university_important'] = df['university_important'].replace([1], 9)
    return df


# democracy: women have the same rights as men
# 0 = an essential characteristic of democracy
# 9 = it's against democracy
def dem_same_rights(df):
    # remove missing
    df['dem_same_rights'] = df['E233']
    df = df[df.dem_same_rights != -5]
    df = df[df.dem_same_rights != -4]
    df = df[df.dem_same_rights != -3]
    df = df[df.dem_same_rights != -2]
    df = df[df.dem_same_rights != -1]
    # recode
    # 0 = an essential characteristic of democracy
    # 9 = it's against democracy
    df['dem_same_rights'] = df['dem_same_rights'].replace([0], 1)
    i = 10
    while i > 0:
        df['dem_same_rights'] = df['dem_same_rights'].replace([i], i * -1)
        i = i - 1
    i = 10
    while i > 0:
        df['dem_same_rights'] = df['dem_same_rights'].replace([-1 * i], i - 1)
        i = i - 1
    return df


# important for successful marriage: sharing household chores
# 0 = very important
# 9 = not very important
def imp_marry_chores(df):
    # remove missing
    df['imp_marry_chores'] = df['D037']
    df = df[df.imp_marry_chores != -5]
    df = df[df.imp_marry_chores != -4]
    df = df[df.imp_marry_chores != -3]
    df = df[df.imp_marry_chores != -2]
    df = df[df.imp_marry_chores != -1]
    # recode
    # 0 = very important
    # 4.5 = rather important
    # 9 = not very important
    df['imp_marry_chores'] = df['imp_marry_chores'].replace([1], 0)
    df['imp_marry_chores'] = df['imp_marry_chores'].replace([2], 4.5)
    df['imp_marry_chores'] = df['imp_marry_chores'].replace([3], 9)
    return df


# sexism score
# 0 = least sexist
# 9 = most sexist
def sexism(df):
    df = men_better_leaders(df)
    df = men_better_executives(df)
    df = dem_same_rights(df)
    df = imp_marry_chores(df)
    df['sexism'] = (df['men_better_leaders'] +
                    df['men_better_executives'] +
                    df['imp_marry_chores'] +
                    df['dem_same_rights']) / 4
    return df
