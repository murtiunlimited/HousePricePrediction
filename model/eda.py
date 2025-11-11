import pandas as pd
import numpy as np

df = pd.read_csv("Bengaluru_House_Data.csv")
df = df.drop(['area_type', 'society', 'balcony', 'availability'], axis='columns')
df = df.dropna()


df['bhk'] = df['size'].apply(lambda x: int(x.split(' ')[0]))

# Convert total_sqft ranges to numbers
def convert_sqft_to_num(x):
    try:
        tokens = x.split('-')
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[1])) / 2
        return float(x)
    except:
        return None

df['total_sqft'] = df['total_sqft'].apply(convert_sqft_to_num)
df = df[df['total_sqft'].notnull()]

df['price_per_sqft'] = df['price'] * 100000 / df['total_sqft']


df['location'] = df['location'].apply(lambda x: x.strip())
location_stats = df['location'].value_counts(ascending=False)
location_stats_less_than_10 = location_stats[location_stats <= 10]
df['location'] = df['location'].apply(lambda x: 'other' if x in location_stats_less_than_10 else x)


df = df[~(df.total_sqft / df.bhk < 300)]

def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df = subdf[(subdf.price_per_sqft > (m - st)) & (subdf.price_per_sqft <= (m + st))]
        df_out = pd.concat([df_out, reduced_df], ignore_index=True)
    return df_out

df = remove_pps_outliers(df)

def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('bhk'):
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }
        for bhk, bhk_df in location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk - 1)
            if stats and stats['count'] > 5:
                exclude_indices = np.append(
                    exclude_indices,
                    bhk_df[bhk_df.price_per_sqft < stats['mean']].index.values
                )
    return df.drop(exclude_indices, axis='index')

df = remove_bhk_outliers(df)

df = df[df.bath < df.bhk + 2]


df = df.drop(['size', 'price_per_sqft'], axis='columns')
dummies = pd.get_dummies(df.location)
df = pd.concat([df, dummies.drop('other', axis='columns')], axis='columns')
df = df.drop('location', axis='columns')
print(df.shape)

df.to_csv("Data_cleaned.csv", index=False)
print("EDA complete. Cleaned dataset saved as 'Data_cleaned.csv'")
