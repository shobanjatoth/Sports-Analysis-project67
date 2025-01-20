import pandas as pd

def preprocess(df):
    # filtering for summer olympics
    # df = df[df['Season'] == 'Summer']
    # # merge with region_df
    # df = df.merge(region_df, on='NOC', how='left')
    # # dropping duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df

def ipl(data):
    # data2=data2.rename(columns={"match_id":"id"})
    # # merge with region_df
    # data= data.merge(data2, on='id', how='left')
    # dropping duplicates
    data.drop_duplicates(inplace=True)

    return data

def tornmet(data1):
     data1 = pd.read_csv("datasets/tornament.csv")
     return data1