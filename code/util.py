"""
util.py contains custom functions:
    1. download_file: Download the .csv file from the given link and read as dataframe
    2. delete_files: Delete files in the given folder, except README.md
    3. missing_detect: Detect if any missing value for each variable
    4. variable_dist: Generate plots of variables' distribution and save
    5. q1_sale_growth_by_year: Generate plots of Q1 and save
    6. q23_sale_growth: Generate plots of Q2 or Q3 and save
"""
import requests
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import math

# download_file(url, output)
def download_file(url=None, output=r'../public/output'):
    """ Download the .csv file from the given link and read as dataframe

    Args: 
        url: str
        output: path to store downloaded files
    
    Returns:
        DataFrame
    """
    local_filename = os.path.join(output, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return pd.read_csv(local_filename)

# delete_files(path, keep)
def delete_files(path=r'../public/output', keep=['README.md']):
    """ Delete files in the given folder path, except README.md

    Args:
        path: path, starting with r''
        keep: files to keep, default value as README.md

    Returns:
        nothing to return
    """
    for fname in os.listdir(path):
        if fname not in (keep):
            os.remove(os.path.join(path, fname))
    return

# missing_detect()
def missing_detect(df=None, cols=None):
    """ Detect if any missing value for each variable

    Args:
        df: input dataframe
        cols: columns from the input dataframe, df.columns

    Returns:
        return True if no missing values; otherwise, return False and variables with missing value
    """
    cols, res = list(cols), []
    for col in cols:
        if getattr(df, col).isna().sum() != 0:
            res.append(col)
    if len(res) == 0:
        print(f"No missing values!")
        return True, res
    else:
        print(f"Missing values in {res}")
        return False, res
    
# variable_dist():
def variable_dist(df=None, cols=None, countplot=['store'], fname='variable_dist.png',
                  output=r'../public/output', subplots=[1,4], figsize=(20,6)):
    """ Generate plots of variables' distribution and save

    Args:
        df: input dataframe
        cols: columns from the input dataframe, df.columns

    Returns:
        Nothing to return
    """
    sns.set()
    fig, axes = plt.subplots(subplots[0], subplots[1], figsize=figsize)
    ax, i, cols = axes.flatten(), 0, list(cols)
    for col in cols:
        if col in countplot:
            temp = sns.countplot(data=df, x=col, ax=ax[i])
            temp.set(xlabel=col, ylabel='Count of {col}', title=f"Countplot of {col}")
        else:
            temp = sns.histplot(getattr(df, col), kde=True, color='purple', ax=ax[i])
            temp.set(xlabel=col, ylabel='Density', title=f"Histogram of {col}")
        i += 1
    plt.tight_layout()
    plt.savefig(os.path.join(output, fname))
    return fname

# q1_sale_growth_by_year()
def q1_sale_growth_by_year(df=None, fname='q1_sale_growth_year.png', output=r'../public/output',
                           subplots=[2,2], figsize=(40,20), periods=['year', 'month'], cats=['sales', 'growth']):
    """ Generate plots of sales & growth by year/month and save

    Args:
        df: input dataframe

    Returns:
        fname
    """
    sns.set()
    fig, axes = plt.subplots(subplots[0], subplots[1], figsize=figsize)
    ax, i = axes.flatten(), 0
    for cat in cats:
        for period in periods:
            if cat.lower() == 'sales':
                data_df = df[[period, cat]].groupby(by=[period]).sum().reset_index()
                data_df[cat] = data_df[cat].apply(lambda x: float(format(x/1000000, '.2f')))
                temp = sns.lineplot(data=data_df, x=period, y=cat, ax=ax[i])
                temp.set(xlabel=period, ylabel=f"{cat} (M)", title=f"{cat.capitalize()} Trend by {period.capitalize()} (M)")
                if period == 'month':
                    temp.set_xticklabels(temp.get_xticklabels(), rotation=45)
            elif cat.lower() == 'growth':
                variable = 'sales'
                data_df = df[[period, variable]].groupby(by=[period]).sum().reset_index()
                data_df[cat] = (data_df[variable].diff()/data_df[variable].shift(1))
                data_df.dropna(inplace=True)
                data_df[cat] = data_df[cat].apply(lambda x: float(format(x*100, '.2f')))
                temp = sns.lineplot(data=data_df, x=period, y=cat, ax=ax[i])
                temp.set(xlabel=period, ylabel=f"{cat} (%)", title=f"{cat.capitalize()} Trend by {period.capitalize()} (%)")
                if period == 'month':
                    temp.set_xticklabels(temp.get_xticklabels(), rotation=45)
            i += 1
    plt.tight_layout()
    plt.savefig(os.path.join(output, fname))
    return fname

# q23_sale_growth(): Generate plots of Q2/Q3 and save
def q23_sale_growth(df=None, fname='q2_sale_growth_store.png', output=r'../public/output', key_0=2,
                           subplots=[2,2], figsize=(40,20), periods=['year', 'month'], cats=['sales', 'growth']):
    """ Generate plots of sales & growth by store or items and save

    Args:
        df: input dataframe

    Returns:
        fname
    """
    sns.set()
    fig, axes = plt.subplots(subplots[0], subplots[1], figsize=figsize)
    ax, i = axes.flatten(), 0
    if key_0 == 2:
        key = 'store'
    elif key_0 == 3:
        key = 'item'
    for cat in cats:
        for period in periods:
            if cat.lower() == 'sales':
                data_df = df[[key, period, cat]].groupby(by=[key, period]).sum().reset_index()
                if key == 'item':
                    data_df[cat] = data_df[cat].apply(lambda x: float(format(x/1000, '.2f')))
                else:
                    data_df[cat] = data_df[cat].apply(lambda x: float(format(x/1000000, '.2f')))
                temp = sns.lineplot(data=data_df, x=period, y=cat, hue=key, ax=ax[i])
                if key == 'item':
                    temp.set(xlabel=period, ylabel=f"{cat} (K)", title=f"{cat.capitalize()} Trend by {period.capitalize()} (K)")
                else:
                    temp.set(xlabel=period, ylabel=f"{cat} (M)", title=f"{cat.capitalize()} Trend by {period.capitalize()} (M)")
                if period == 'month':
                    temp.set_xticklabels(temp.get_xticklabels(), rotation=45)
            elif cat.lower() == 'growth':
                variable = 'sales'
                data_df = df[[key, period, variable]].groupby(by=[key, period]).sum().reset_index()
                data_df[cat] = (data_df[variable].diff()/data_df[variable].shift(1))
                if period == 'year':
                    data_df.loc[getattr(data_df,period)=='2013', [cat]] = math.nan
                if period == 'month':
                    data_df.loc[getattr(data_df,period)=='2013-01', [cat]] = math.nan
                data_df.dropna(inplace=True)
                data_df[cat] = data_df[cat].apply(lambda x: float(format(x*100, '.2f')))
                temp = sns.lineplot(data=data_df, x=period, y=cat, hue=key, ax=ax[i])
                temp.set(xlabel=period, ylabel=f"{cat} (%)", title=f"{cat.capitalize()} Trend by {period.capitalize()} (%)")
                if period == 'month':
                    temp.set_xticklabels(temp.get_xticklabels(), rotation=45)
            i += 1
    plt.tight_layout()
    plt.savefig(os.path.join(output, fname))
    return fname