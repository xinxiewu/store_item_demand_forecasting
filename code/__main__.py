"""
__maim__.py contains the workflow to run all sub-programs
"""
from util import *

def main(fileurl=None, output=None):
    """
    Step 1: Data Preparation & EDA
    """
    # 1.1 Download dataset from Github & read as DataFrame
    df = download_file(fileurl)
    print(f"Loaded dataset with {df.shape}\n")
    # 1.2 EDA
    # 1.2.1 Variable Distributions (outlier & extreme) & Missing Values
    print(f"EDA Part")
    miss_yn, miss = missing_detect(df=df,cols=df.columns)
    fname = variable_dist(df=df, cols=df.columns)
    print(f"Variables' original distribution saved as {fname}")
    """No need of correlation heatmap"""
    df['year'] = pd.to_datetime(df['date']).apply(lambda x: str(x)[:4])
    df['month'] = pd.to_datetime(df['date']).apply(lambda x: str(x)[:7])

    # 1.2.2 Sales Trend and Growth Rate Over the 5 Years
    fname = q1_sale_growth_by_year(df=df)
    print(f"Q1 plot saved as {fname}")
    # 1.2.3 Sales Trend by Different Stores

    # 1.2.4 Sales Trend by Different Items

    # 1.2.5 Recommendations for Stores' Sales Growth

    # 1.2.6 Data Preparation for Modeling

    """
    Step 2: Modeling - Predict 3 months' sales for these 50 different items at 10 stores
    """


if __name__ == '__main__':
    """
    Step 1: Clean output folder
    """
    delete_files()
    """
    Step 2: Call the main program
    """
    # main(fileurl = 'https://raw.githubusercontent.com/xinxiewu/datasets/main/store_item_demand/storedata.csv',
    #      output = r'../public/output'
    #      )