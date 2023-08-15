"""
__maim__.py contains the workflow to run all sub-programs
"""
import os
from util import *
import warnings
warnings.filterwarnings("ignore")

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
    print(f"No need of correlation heatmap")
    df['year'] = pd.to_datetime(df['date']).dt.strftime('%Y')
    df['month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
    # 1.2.2 Sales Trend and Growth Rate Over the 5 Years
    fname = q1_sale_growth_by_year(df=df)
    print(f"Q1 plot saved as {fname}")
    # 1.2.3 Sales Trend by Different Stores
    fname = q23_sale_growth(df=df)
    print(f"Q2 plot saved as {fname}")
    # 1.2.4 Sales Trend by Different Items
    fname = q23_sale_growth(df=df, fname='q3_sale_growth_item.png', key_0=3)
    print(f"Q3 plot saved as {fname}")
    # 1.2.5 Recommendations for Stores' Sales Growth
    print(f"Q4 Recommendation: Work hard!")
    # 1.2.6 Data Preparation for Modeling
    df = df[['month', 'store', 'item', 'sales']].groupby(by=['month', 'store', 'item']).sum().reset_index()
    df.to_csv(os.path.join(output, 'data_final.csv'), index=False)
    print(f"Dataset is READY!\n")

    """
    Step 2: Time Series Modeling - Predict 3 months' sales for these 50 different items at 10 stores
    """


if __name__ == '__main__':
    """
    Step 1: Clean output folder
    """
    delete_files()
    """
    Step 2: Call the main program
    """
    main(fileurl = 'https://raw.githubusercontent.com/xinxiewu/datasets/main/store_item_demand/storedata.csv',
         output = r'../public/output'
         )