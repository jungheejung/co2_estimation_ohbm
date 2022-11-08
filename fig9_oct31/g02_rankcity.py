# %%
import os 
import glob
from pathlib import Path
import shutil
import re
import pandas as pd
# %%
current_dir = os.getcwd()
main_dir = Path(current_dir).parents[0]
input_dir = os.path.join(main_dir, 'fig9_oct31')
# %%

co2_df = pd.DataFrame(columns={'city', 'country', 'location','co2'})
key_city = pd.read_csv(os.path.join(input_dir, 'Large_airports_key.csv'))
for index, row in key_city.iterrows():
    key_city.iloc[index, 2] = str(row['location'].replace(" ", ""))
dest_city = key_city['location']
citylist = sorted(os.listdir(os.path.join(input_dir, 'input_ohbm')))
new_df = pd.read_csv(os.path.join(main_dir, 'INPUT_ohbm_171819_freq.csv'))
new_df.rename(columns = {'City': 'city', 'Country': 'country'}, inplace = True)

# %%
# cleanlist = citylist.remove('.DS_Store')
cleanlist = []
cleanlist[:] = [x for x in citylist if '.DS_Store' not in x]


example= pd.read_csv('/Users/h/Dropbox/projects_dropbox/other_sideprojects/green_climatechange/fig9_oct31/output/Amsterdam_Netherlands.csv')

# co2_df 
# row: destination
# column: input ohbm
co2_df = pd.DataFrame(data = None, 
    index = example['location'],
    columns = new_df['city'].tolist() )
co2_df.sort_index(inplace = True)
# %%
for ind, fname in enumerate(cleanlist):
    # city, cumulative co2
# iloc sum co2 based on frequencies 
# save it to cumulativeco2perdest
    # parameters _________________________________________________________________________________
    if not fname.startswith('.') and os.path.splitext(fname)[1] == '.csv':

        city = os.path.splitext(fname)[0]
        print(city)
        output = pd.DataFrame()
        output= pd.read_csv(os.path.join(input_dir, 'output', fname ))
        output['trips_amount'] = output['plane trips_amount'] + output['train trips_amount']
        output['correct_co2_kg'] = output['co2_kg']/output['trips_amount']
        frequency = new_df.loc[new_df['city']  == city.split('_')[0], 'Freq'].tolist()[0]
        # find city name in new_df, then grab freq
        print(frequency)
        output['co2_mul_attendee'] = output['correct_co2_kg'] * frequency * 2
        out = output.set_index('location')
        out_co2 = out[['co2_mul_attendee']].copy()
        out_co2.sort_index(inplace = True)
        co2_df.iloc[:,co2_df.columns.get_loc(city.split('_')[0])] = out_co2

        
        # co2_df.insert(co2_df.columns.get_loc(city.split('_')[0]), 
        # column = city.split('_')[0],  
        # value = pd.Series(out_co2), 
        # index=out.index)


        # # merged = pd.merge(co2_df, out['co2_mul_attendee'], left_index=True, right_on='location')
        # final = co2_df.merge(out_co2, on=city.split('_')[0], how='co2_df')
        # # sort by country 
        # co2_df[[city.split('_')[0]]].merge(out_co2, on='location', how='right')

        # output_freq = output.merge(new_df, how = 'left', on = 'city')
        # output_freq['co2_mul_attendeed'] = output_freq['co2_kg'] * output_freq['Freq']
        # ISSEU: TODO: the calculator suposely does not incorporate frequency of attendees. 
        # it seems to collapse and only grab unique values (500 new york is calculated as 1 new york attendeed)
        # manually, I need to account for attendees

        # co2_df.loc[ind, 'co2'] = output['co2_mul_attendeed'].sum()
        # co2_df.loc[ind, 'location'] = city

    # co2_df['city'] = co2_df.location.str.split('_ ', expand = True)[0]
    # co2_df['country'] = co2_df.location.str.split('_ ', expand = True)[1]
    # co2_df.sort_values(by=['co2'], inplace = True)

# %%
co2_df['sum_co2kg'] = co2_df.iloc[:, range(len(new_df['city'].tolist()))].sum(axis=1)
co2_df['sum_co2kg_div_3'] = co2_df['sum_co2kg']/3
co2_df['weightedsum_co2ton'] = co2_df['sum_co2kg_div_3']/1000
# %%
co2_df.to_csv(os.path.join(main_dir, 'fig9_oct31','OUTPUT_g02_rank_city.csv'), index = True)


# %%


