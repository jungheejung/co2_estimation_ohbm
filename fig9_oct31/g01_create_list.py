# %%
import pandas as pd
import numpy as np
import os
# load csv
# %%
fname = '/Users/h/Dropbox/projects_dropbox/other_sideprojects/green_climatechange/fig9_oct31/Large_airports_key.csv'
save_dir = '/Users/h/Dropbox/projects_dropbox/other_sideprojects/green_climatechange/fig9_oct31/input'
airport = pd.read_csv(fname)

# grab each row
for index, row in airport.iterrows():
    new_df = pd.DataFrame(columns = ['City', 'Country'], index = range(len(airport)))
    airport.iloc[index, 2] = str(row['location'].replace(" ", ""))
    # pd.concat(pd.Series(row[['City', 'Country']])*len(airport))
    new_df['City'] = row['City']
    new_df['Country'] = row['Country']
    save_name = os.path.join(save_dir, f"{row['location']}.csv")
    new_df.to_csv(save_name,index=False)



# remove any space
# copy with length
# populate and save

# key.csv -> INPUTDIR -> estimate via website -> OUTPUTDIR -> calculate average via green_rankcity.py
# %%
# concatenate all input
input_dir = '/Users/h/Dropbox/projects_dropbox/other_sideprojects/green_climatechange/fig9_oct31/'
csvlist =os.listdir(os.path.join(input_dir,'input') )
concat_df = pd.DataFrame()
# flat_list = [item for sublist in csvlist for item in sublist]
for ind, fname in enumerate(csvlist):
    if os.path.splitext(fname)[1] == '.csv':
        df= pd.read_csv(os.path.join(os.path.join(input_dir,'input'), fname))
        concat_df = pd.concat([concat_df,df], ignore_index=True)
concat_df.to_csv(os.path.join(input_dir, 'input_long', 'allairport_input.csv'), index=None)
    # 
# concatenate key 152 times
# %%
key_csv = '/Users/h/Dropbox/projects_dropbox/other_sideprojects/green_climatechange/fig9_oct31/Large_airports_key.csv'
key_df = pd.read_csv(key_csv)
len(key_df)
key_stack = pd.concat([key_df]*len(key_df))
key_stack.to_csv(os.path.join(input_dir, 'dest_long', 'allairport_dest.csv'), index=None)
# %%

i = 1
for x in np.array_split(key_stack, 40, axis=0):
    print('Processing df... ', i)
    x.to_csv(os.path.join(input_dir, 'dest_long', f'allairport_dest_chunk{i:02d}.csv'), index=None)
    i += 1

# %%
input = pd.read_csv(os.path.join(input_dir, 'input_long', 'allairport_input.csv'))
i = 1
for x in np.array_split(input, 40, axis=0):
    print('Processing df... ', i)
    x.to_csv(os.path.join(input_dir, 'input_long', f'allairport_dest_chunk{i:02d}.csv'), index=None)
    i += 1
# %%
