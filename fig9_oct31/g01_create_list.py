# %%
import pandas as pd
import numpy as np
import os
# load csv
# %%
key_fname = '/Users/h/Dropbox/projects_dropbox/other_sideprojects/green_climatechange/fig9_oct31/Large_airports_key.csv'
fname = '/Users/h/Dropbox/projects_dropbox/other_sideprojects/green_climatechange/fig9_oct31/INPUT_ohbm_171819_freq.csv'
save_dir = '/Users/h/Dropbox/projects_dropbox/other_sideprojects/green_climatechange/fig9_oct31/input_ohbm'
airport = pd.read_csv(fname)
keyairport = pd.read_csv(key_fname)

# grab each row
for index, row in airport.iterrows():
    new_df = pd.DataFrame(columns = ['City', 'Country'], index = range(len(keyairport)))
    # airport.iloc[index, 2] = str(row['location'].replace(" ", ""))
    # pd.concat(pd.Series(row[['City', 'Country']])*len(airport))
    new_df['City'] = row['City']
    new_df['Country'] = row['Country']
    save_name = os.path.join(save_dir, f"{row['City']}_{row['Country']}.csv")
    new_df.to_csv(save_name,index=False)